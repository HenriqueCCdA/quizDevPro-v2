from django.shortcuts import render, redirect, reverse
from django.utils.timezone import now

from quiz.base.forms import AlunoForm
from quiz.base.models import Pergunta, Aluno, Resposta


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


PONTUACAO_MAXIMA = 1000


def pergunta(request, slug):

    indice = int(slug)
    try:
        aluno_id = request.session['aluno_id']

    except KeyError:
        return redirect(reverse('base:home'))

    else:

        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice-1]

        except IndexError:
            return redirect(reverse('base:classificacao'))

        else:
            contexto = {'indice_pergunta': indice,
                        'pergunta': pergunta}
            if request.method == 'POST':
                resposta_indice = int(request.POST['indice_resposta'])
                if resposta_indice == pergunta.alternativas_correta:
                    # Armazenar dados da respota
                    try:
                        data_da_primeira_resposta = Resposta.objects.filter(pergunta_id=pergunta.id
                                                                            ).order_by('respondida_em')[0].respondida_em
                    except IndexError:
                        pontos = PONTUACAO_MAXIMA
                        # Resposta(aluno_id=aluno_id, pergunta_id=pergunta.id, pontos=PONTUACAO_MAXIMA).save()
                    else:
                        diferenca_em_segundos = int((now() - data_da_primeira_resposta).total_seconds())
                        pontos = max(PONTUACAO_MAXIMA - diferenca_em_segundos, 10)
                    finally:
                        Resposta(aluno_id=aluno_id, pergunta_id=pergunta.id, pontos=pontos).save()

                    return redirect(reverse('base:pergunta',  kwargs={'slug': indice + 1}))
                contexto['indice_resposta'] = resposta_indice

            return render(request, 'base/pergunta.html', contexto)


def classificacao(request):
    return render(request, 'base/classificacao.html')
