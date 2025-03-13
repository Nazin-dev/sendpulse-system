from django.shortcuts import render, redirect
from django.urls import reverse
from send.scripts import clients, api
from send.scripts.redis_client import redis_client

def home(request):
    if request.method == "POST":
        # Modo POST: Criação ou atualização da campanha
        campaign_id = request.POST.get("campaign_id")  # Vazio para nova campanha
        campaign_name = request.POST.get("name", "")
        dias = request.POST.get("dias", 2)
        text_message = request.POST.get("text-message", "")
        
        try:
            dias = int(dias)
        except ValueError:
            dias = 2

        # Busca os clientes para envio; se em edição, filtra os excluídos via Redis,
        # caso contrário, aplica exclusões armazenadas na sessão (para nova campanha)
        clientes_list = clients.get_clientes(dias, campaign_id if campaign_id else None)
        if not campaign_id:
            session_exclusions = request.session.get("new_campaign_exclusions", [])
            clientes_list = [c for c in clientes_list if str(c["codigo_cliente"]).strip() not in session_exclusions]
    
        phone_numbers = []
        for cliente in clientes_list:
            telefone = cliente['telefone'].strip()
            if not telefone.startswith('+55'):
                telefone = '+55' + telefone
            phone_numbers.append(telefone)

        if campaign_id:
            # Atualiza campanha existente
            key = f"campaign:{campaign_id}"
            redis_client.hset(key, mapping={
                "name": campaign_name,
                "dias": dias,
                "message": text_message
            })
            print(f"Campanha {campaign_id} atualizada.")
        else:
            # Cria nova campanha
            api.send_sms(phone_numbers, text_message)
            new_campaign_id = redis_client.incr("campaign_id_counter")
            redis_client.hset(f"campaign:{new_campaign_id}", mapping={
                "name": campaign_name,
                "dias": dias,
                "message": text_message,
                "status": "active"
            })
            redis_client.sadd("campaigns", new_campaign_id)
            print("Nova campanha criada.")
            # Salva as exclusões da sessão no Redis para esta nova campanha
            session_exclusions = request.session.get("new_campaign_exclusions", [])
            for code in session_exclusions:
                redis_client.sadd(f"excluded_clients:{new_campaign_id}", code)
            request.session["new_campaign_exclusions"] = []

        return redirect('campanhas')

    else:
        # Modo GET: Carrega os dados para edição ou preserva os valores digitados
        edit_campaign_id = request.GET.get("edit_campaign_id")
        initial_data = {}
        if edit_campaign_id:
            key = f"campaign:{edit_campaign_id}"
            data = redis_client.hgetall(key)
            if data:
                campaign = {k.decode(): v.decode() for k, v in data.items()}
                campaign["id"] = edit_campaign_id
                initial_data = campaign
        else:
            # Para nova campanha, usa os valores da query string (se houver)
            initial_data = {
                "name": request.GET.get("name", ""),
                "dias": request.GET.get("dias", ""),
                "message": request.GET.get("text-message", "")
            }
        
        # Usa o valor de "dias" salvo ou da query string; se não houver, default para 2
        dias_str = initial_data.get("dias")
        if not dias_str:
            dias_str = request.GET.get('dias')
        if not dias_str:
            dias_str = "2"
        try:
            dias = int(dias_str)
        except ValueError:
            dias = 2

        campaign_id_for_filter = initial_data.get("id") if initial_data.get("id") else None
        clientes_list = clients.get_clientes(dias, campaign_id_for_filter)
        if not campaign_id_for_filter:
            session_exclusions = request.session.get("new_campaign_exclusions", [])
            clientes_list = [c for c in clientes_list if str(c["codigo_cliente"]).strip() not in session_exclusions]
    
        context = {
            'clientes': clientes_list,
            'dias': dias,
            'placeholder': 'Digite o texto da campanha',
            'initial': initial_data,
        }
        return render(request, 'pages/index.html', context)

def remove_cliente(request, codigo_cliente):
    # Se estivermos em modo de edição, usamos o parâmetro "edit_campaign_id"
    campaign_id = request.GET.get("edit_campaign_id")
    if campaign_id:
        clients.remove_from_clientes(codigo_cliente, campaign_id)
        return redirect(f"{reverse('home')}?edit_campaign_id={campaign_id}")
    else:
        # Modo nova campanha: armazena a exclusão na sessão
        exclusions = request.session.get("new_campaign_exclusions", [])
        code = str(codigo_cliente).strip()
        if code not in exclusions:
            exclusions.append(code)
        request.session["new_campaign_exclusions"] = exclusions
        # Preserve os parâmetros da query string para que os campos não sumam
        query = request.GET.urlencode()
        if query:
            return redirect(f"{reverse('home')}?{query}")
        return redirect('home')
