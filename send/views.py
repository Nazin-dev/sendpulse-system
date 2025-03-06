from django.shortcuts import render, redirect
from . import clients

def home(request):
    # Pega o valor do parâmetro 'dias'; se não houver, usa 2 como padrão.
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
