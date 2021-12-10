from django.db.models import Sum

from quiz.base.models import Resposta, Pergunta


def calcula_a_pontuacao_do(aluno_id: int) -> int:
    """
    Calcula a pontudação para um determinado aluno
    :param aluno_id: Id do aluno
    :return: Retorna a pontuação do aluno_id
    """
    return Resposta.objects.filter(aluno_id=aluno_id).aggregate(Sum('pontos'))['pontos__sum']


def calcula_o_numero_de_alunos_com_pontuacao_maior_que(pontos: int) -> int:
    """
    Calcula o numero de alunos com a pontuação maioque que pontos
    :param pontos: pontuação desejada
    :return: retorna o numero de alunos com pontuação maior
    """
    return Resposta.objects.values('aluno').annotate(Sum('pontos')).filter(pontos__sum__gt=pontos).count()


def lista_de_alunos(numero_de_alunos: int = 5):
    """
    Retorna a lista dos n primeiros alunos
    :param numero_de_alunos: numero de alunos
    :return: lista de alunos em ordem crescente
    """
    return list(Resposta.objects.values('aluno', 'aluno__nome')
                .annotate(Sum('pontos'))
                .order_by('-pontos__sum')[:numero_de_alunos])


def numero_repostas_respondidas(aluno_id: int) -> int:
    """
    Retorna numero resposta_respondidas pelo um aluno
    :param aluno_id: Id do aluno
    :return: numero_repostas_respondidas pelo aluno
    """

    return Resposta.objects.filter(aluno_id=aluno_id).count()


def quiz_finalizado(aluno_id: int) -> bool:
    """
    Retorna se o quiz foi finalizado ou não pelo aluno
    :param aluno_id: Id do aluno
    :return: True e False
    """

    return numero_repostas_respondidas(aluno_id) == numero_de_perguntas_ativas()


def numero_de_perguntas_ativas() -> int:
    """
    Retorna o numero de perguntas ativas.
    :return:  Retorna de perguntas
    """
    return Pergunta.objects.filter(disponivel=True).count()
