from django.shortcuts import render, redirect, reverse

from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta


def home(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('base:pergunta',  kwargs={'slug': 1}))

    return render(request, 'base/home.html')


def pergunta(request, slug):

    question = list(Pergunta.objects.filter(disponivel=True, id=slug))

    data = {'question_index': slug}

    if question:  # is not empty
        question = question[0]
        data['question'] = question

    return render(request, 'base/pergunta.html', data)


def classificacao(request):
    return render(request, 'base/classificacao.html')
