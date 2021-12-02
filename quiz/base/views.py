from django.shortcuts import render, redirect, reverse

from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta, Aluno


def home(request):

    if request.method == 'POST':

        # Usuario já existe
        email = request.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:

            # Usuário não existe
            form = AlunoForm(request.POST)
            if form.is_valid():
                aluno = form.save()
                request.session['aluno_id'] = aluno.id
                return redirect(reverse('base:pergunta',  kwargs={'slug': 1}))
            else:
                contexto = {'formulario': form}
                return render(request, 'base/home.html', contexto)

        else:
            request.session['aluno_id'] = aluno.id
            return redirect(reverse('base:pergunta',  kwargs={'slug': 1}))

    return render(request, 'base/home.html')


def pergunta(request, slug):

    try:
        request.session['aluno_id']

    except KeyError:
        return redirect(reverse('base:home'))

    else:

        pergunta = list(Pergunta.objects.filter(disponivel=True, id=slug))
        contexto = {'question_index': slug}
        if pergunta:  # is not empty
            pergunta = pergunta[0]
            contexto['question'] = pergunta

        if request.method == 'POST':
            resposta_indice = int(request.POST['resposta_indice'])
            if resposta_indice == pergunta.alternativas_correta:
                # Armazenar dados da respota
                return redirect(reverse('base:pergunta',  kwargs={'slug': int(slug) + 1}))
            contexto['resposta_indice'] = resposta_indice

        return render(request, 'base/pergunta.html', contexto)


def classificacao(request):
    return render(request, 'base/classificacao.html')
