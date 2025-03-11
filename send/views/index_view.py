from django.shortcuts import render, redirect
from send.scripts import clients
from send.scripts import api

def home(request):
    if request.method == "POST":
        text_message = request.POST.get("text-message")
        # Recupera o valor de 'dias' enviado junto com o formulário (campo oculto)
        dias = request.POST.get("dias", 2)
        try:
            dias = int(dias)
        except ValueError:
            dias = 2

        # Obtém os clientes com base no parâmetro 'dias'
        clientes = clients.get_clientes(dias)
        # Extrai os telefones e adiciona o código +55 caso não esteja presente
        phone_numbers = []
        for cliente in clientes:
            telefone = cliente['telefone'].strip()
            if not telefone.startswith('+55'):
                telefone = '+55' + telefone
            phone_numbers.append(telefone)
        
        # Chama a função de envio de SMS passando os telefones e a mensagem digitada
        # Substitua phone_numbers [+5589981350933]
        api.send_sms([], text_message)
        print("Mensagem recebida:", text_message)
        return redirect('home')
    else:
        dias = request.GET.get('dias', 2)
        try:
            dias = int(dias)
        except ValueError:
            dias = 2

        clientes = clients.get_clientes(dias)
    
        context = {
            'clientes': clientes,
            'dias': dias,
            'placeholder': 'Hello, World'
        }
        return render(request, 'pages/index.html', context)

def remove_cliente(request, codigo_cliente):
    """
    Marca o cliente no conjunto de excluídos (apenas em memória)
    e redireciona para home.
    """
    clients.remove_from_clientes(codigo_cliente)
    return redirect('home')
