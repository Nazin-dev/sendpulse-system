from django.shortcuts import render
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
        'dias': dias  
    }
    return render(request, 'pages/index.html', context)
