from django.shortcuts import render, redirect
from  send.scripts import clients
from send.scripts import api

def home(request):
    if request.method == "POST":
        text_message = request.POST.get("text-message")
        # Aqui estou usando a função para enviar as mensagens
        api.send_sms(["+5589981350933"], text_message)
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
    e redireciona de volta para home.
    """
    clients.remove_from_clientes(codigo_cliente)
    return redirect('home')

