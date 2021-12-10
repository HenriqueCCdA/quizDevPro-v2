import pytest
from model_bakery import baker

from quiz.base.models import Resposta, Pergunta
from quiz.base.facade import numero_repostas_respondidas, quiz_finalizado, numero_de_perguntas_ativas

N_REPOSTAS = 5
N_PERGUNTAS_ATIVAS = 10
N_PERGUNTAS_INATIVAS = 5


@pytest.fixture
def perguntas(um_aluno_db):
    return (baker.make(Pergunta, N_PERGUNTAS_ATIVAS, disponivel=True),
            baker.make(Pergunta, N_PERGUNTAS_INATIVAS, disponivel=False))


@pytest.fixture
def respostas(um_aluno_db):
    return (baker.make(Resposta, N_REPOSTAS, aluno=um_aluno_db),
            baker.make(Resposta, N_REPOSTAS, aluno=um_aluno_db))


def test_o_numero_perguntas_respondidas_pelo_aluno_ativo(perguntas, um_aluno_db):
    """
    Testa o numero de perguntas respondidas pelo o aluno ativo
    """
    perguntas_ativas = perguntas[0]

    for pergunta in perguntas_ativas[:N_REPOSTAS]:
        Resposta(aluno_id=um_aluno_db.id, pergunta_id=pergunta.id, pontos=1).save()

    numero_repostas_repondidas = numero_repostas_respondidas(um_aluno_db.id)
    flag = quiz_finalizado(um_aluno_db.id)

    assert not flag
    assert numero_repostas_repondidas == N_REPOSTAS


def test_se_o_aluno_ja_respondeu_todas_as_perguntas(perguntas, um_aluno_db):
    """
    Testa se o aluno ja respondeu todas as perguntas ativas
    """

    perguntas_ativas = perguntas[0]
    for pergunta in perguntas_ativas:
        Resposta(aluno_id=um_aluno_db.id, pergunta_id=pergunta.id, pontos=1).save()

    flag = quiz_finalizado(um_aluno_db.id)

    assert flag


def test_o_numero_total_de_perguntas_ativas(perguntas, um_aluno_db):
    """
    Testa o calulo do numero de perguntas ativas
    """

    perguntas_ativas = numero_de_perguntas_ativas()

    assert perguntas_ativas == N_PERGUNTAS_ATIVAS
