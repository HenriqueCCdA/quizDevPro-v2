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
        question = list(Pergunta.objects.filter(disponivel=True, id=slug))

        data = {'question_index': slug}

        if question:  # is not empty
            question = question[0]
            data['question'] = question

    return render(request, 'base/pergunta.html', data)


def classificacao(request):
    return render(request, 'base/classificacao.html')
