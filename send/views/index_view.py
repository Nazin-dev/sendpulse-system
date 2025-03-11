from django.shortcuts import render, redirect
from send.scripts import clients, api
from send.scripts.redis_client import redis_client

def home(request):
    if request.method == "POST":
        # Se estiver editando, haverá o campo oculto "campaign_id"
        campaign_id = request.POST.get("campaign_id")
        campaign_name = request.POST.get("name", "")
        dias = request.POST.get("dias", 2)
        text_message = request.POST.get("text-message", "")
        
        try:
            dias = int(dias)
        except ValueError:
            dias = 2

        # Busca clientes para envio (opcional, se necessário)
        clientes = clients.get_clientes(dias)
        phone_numbers = []
        for cliente in clientes:
            telefone = cliente['telefone'].strip()
            if not telefone.startswith('+55'):
                telefone = '+55' + telefone
            phone_numbers.append(telefone)

        if campaign_id:
            # Modo de edição: atualiza a campanha existente
            key = f"campaign:{campaign_id}"
            redis_client.hset(key, mapping={
                "name": campaign_name,
                "dias": dias,
                "message": text_message
            })
            print(f"Campanha {campaign_id} atualizada.")
        else:
            # Modo de criação: envia SMS (se estiver habilitado) e cria a nova campanha
            api.send_sms(phone_numbers, text_message)
            # Gera um novo ID para a campanha
            campaign_id = redis_client.incr("campaign_id_counter")
            redis_client.hset(f"campaign:{campaign_id}", mapping={
                "name": campaign_name,
                "dias": dias,
                "message": text_message,
                "status": "active"
            })
            redis_client.sadd("campaigns", campaign_id)
            print("Nova campanha criada.")

        return redirect('campanhas')

    else:
        # Se houver o parâmetro "edit_campaign_id" na URL, busca os dados para edição
        edit_campaign_id = request.GET.get("edit_campaign_id")
        initial_data = {}
        if edit_campaign_id:
            key = f"campaign:{edit_campaign_id}"
            data = redis_client.hgetall(key)
            if data:
                # Converte os bytes para string
                campaign = {k.decode(): v.decode() for k, v in data.items()}
                # Adiciona o ID para facilitar o preenchimento
                campaign["id"] = edit_campaign_id
                initial_data = campaign

        dias = request.GET.get('dias', 2)
        try:
            dias = int(dias)
        except ValueError:
            dias = 2

        clientes = clients.get_clientes(dias)
    
        context = {
            'clientes': clientes,
            'dias': dias,
            'placeholder': 'Digite o texto da campanha',
            # Dados da campanha a ser editada, se houver
            'initial': initial_data,
        }
        return render(request, 'pages/index.html', context)

def remove_cliente(request, codigo_cliente):
    clients.remove_from_clientes(codigo_cliente)
    return redirect('home')
