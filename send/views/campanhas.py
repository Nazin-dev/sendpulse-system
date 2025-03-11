from django.shortcuts import render, redirect



def campanhas(request):
    return render(
        request,
        'pages/campanhas.html'
    )