import pytest
from django.test import Client
from model_bakery import baker

from quiz.base.models import Pergunta, Resposta, Aluno


@pytest.fixture
def um_aluno_db(db):
    '''
    Cria uma Aluno e salva no db
    :param db: fixture padrão
    :return: retorna um aluno
    '''
    return baker.make(Aluno)


@pytest.fixture
def uma_pergunta_db(db):
    '''
    Cria uma pergunta ativa e salva no db
    :param db: fixture padrão
    :return: retorna uma pergunta ativa
    '''
    alternatives = ['def', 'func', '@', 'if']
    return baker.make(Pergunta, disponivel=True, alternativas={'array': alternatives})


@pytest.fixture
def uma_reposta_db(um_aluno_db, uma_pergunta_db):
    '''
    Cria a resposta para a pergunta e salva no db
    :param uma_pergunta_db: pergunta ativa
    :return: retorna a resposta
    '''

    return baker.make(Resposta, aluno=um_aluno_db, pergunta=uma_pergunta_db, pontos=300)


@pytest.fixture
def client_login_simpliciado(client: Client, um_aluno_db):
    '''
    Modifica a sessão do cliente para simular o login de usuario.
    :param Client: fixture padrão
    :param db: fixture padrão
    :return: uma istancia de client com a session modificada
    '''
    session = client.session
    session['aluno_id'] = um_aluno_db.id
    session.save()
    session.save()
    return client
