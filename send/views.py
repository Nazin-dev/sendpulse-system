from django.shortcuts import render
import clients

def home(request):
  
  context = {
    'clientes': clients.clientes
  }
  
  return render(
    request,
    'pages/index.html',
    context
   
  )
  
