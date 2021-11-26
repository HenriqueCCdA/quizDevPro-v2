from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def pergunta(request, slug):
    return render(request, 'base/pergunta.html')


def classificacao(request):
    return render(request, 'base/classificacao.html')
