import pytest
from model_bakery import baker

from quiz.base.models import Aluno, Resposta
from quiz.base.facade import calcula_a_pontuacao_do, calcula_o_numero_de_alunos_com_pontuacao_maior_que

PONTOS_ALUNO_ATUAL = 300
OUTROS_ALUNOS = 4
N_REPOSTAS = 5


@pytest.fixture
def repostas_do_aluno_atual(um_aluno_db):
    """
    Cria 4 respostas para a pergunta e salva no db
    :param um_aluno_db: fixture
    :return: retorna as 4 respostas
    """

    return baker.make(Resposta, N_REPOSTAS, aluno=um_aluno_db, pontos=PONTOS_ALUNO_ATUAL)


@pytest.fixture
def outros_alunos():
    """
    Cria 4 alunos e 4 reposta para associado a cada aluno
    """
    alunos = baker.make(Aluno, OUTROS_ALUNOS)

    pontos_alunos = (200, 350, 600, 500)
    for aluno, pontos in zip(alunos, pontos_alunos):
        baker.make(Resposta, N_REPOSTAS, aluno=aluno, pontos=pontos)
    return alunos


def test_pontuacao_total(repostas_do_aluno_atual, um_aluno_db):
    """
    Testa a pontuação total de um aluno
    """
    pontos = calcula_a_pontuacao_do(um_aluno_db.id)
    assert PONTOS_ALUNO_ATUAL * N_REPOSTAS == pontos


def test_a_colocacao_do_aluno(repostas_do_aluno_atual, outros_alunos):
    """
    Testa a colocacao de um aluno em relação os outros
    """
    aluno_id = repostas_do_aluno_atual[0].aluno_id
    pontos = calcula_a_pontuacao_do(aluno_id)
    numero_de_alunos_com_maior_pontuacao = calcula_o_numero_de_alunos_com_pontuacao_maior_que(pontos)
    assert numero_de_alunos_com_maior_pontuacao + 1 == 4
