import pytest
from http import HTTPStatus
from model_bakery import baker

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains
from quiz.base.models import Pergunta


SLUG = 1


@pytest.fixture
def um_pergunta_db(db):
    '''
    Cria uma pergunta ativa
    :param db: fixture padrão
    :return: retorna uma pergunta ativa
    '''
    alternatives = ['def', 'func', '@', 'if']
    return baker.make(Pergunta, disponivel=True, alternativas={'array': alternatives})


@pytest.fixture
def response_sem_usuario_logado(client: Client, um_pergunta_db):
    return client.get(reverse('base:pergunta', kwargs={'slug': SLUG}))


@pytest.fixture
def client_login_simpliciado(client: Client, db):
    '''
    Modifica a sessão do cliente para simular o login de usuario.
    :param Client: fixture padrão
    :param db: fixture padrão
    :return: uma istancia de client com a session modificada
    '''
    session = client.session
    session['aluno_id'] = 1
    session.save()
    session.save()
    return client


@pytest.fixture
def reponse_com_usuario_logado(client_login_simpliciado: Client, um_pergunta_db):
    '''
    Cliente com um usuario logado com apenas um pergunta ativa. Este cliente acesse uma pergunta existente
    :param client_login_simpliciado:
    :param um_pergunta_db:
    :return: response
    '''
    return client_login_simpliciado.get(reverse('base:pergunta', kwargs={'slug': SLUG}))


@pytest.fixture
def reponse_com_usuario_logado_alem_da_ultima_pergunta(client_login_simpliciado: Client, um_pergunta_db):
    '''
    Cliente com um usuario logado com apenas um pergunta ativa. Este cliente acesse uma pergunta não existente
    :param client_login_simpliciado:
    :param um_pergunta_db:
    :return: reponse
    '''
    return client_login_simpliciado.get(reverse('base:pergunta', kwargs={'slug': SLUG+1}))


@pytest.mark.parametrize(('slug', ), [
    (1, ),
    (2, ),
])
def testa_reverse_para_a_pagina_de_pergunta(slug):
    '''
    Testa a funcao reverse para pergunta
    :param slug:
    '''
    assert f'/pergunta/{slug}' == reverse('base:pergunta', kwargs={'slug': slug})


def testa_status_code_pagina_da_pergunta_sem_o_usuario_logado(response_sem_usuario_logado):
    '''
    Testa o redirecionamento da pagina da pergunta quando o usuario não esta logado
    '''
    assert response_sem_usuario_logado.status_code == HTTPStatus.FOUND  # 302
    assert response_sem_usuario_logado.headers['Location'] == reverse('base:home')


def testa_status_code_pagina_da_pergunta_com_o_usuario_logado(reponse_com_usuario_logado):
    '''
    Testa o redirecionamento da pagina da pergunta quando o usuario não esta logado
    '''

    assert reponse_com_usuario_logado.status_code == HTTPStatus.OK  # 302


def testa_o_conteudo_pagina_da_pergunta_com_o_usuario_logado(reponse_com_usuario_logado, um_pergunta_db):
    '''
    Testa o contuedo da paragina da pergunta com o usuario o usuario logado.
    '''
    slug = SLUG

    assert_contains(reponse_com_usuario_logado, f'<h2> Questão {slug} </h2>')
    assert_contains(reponse_com_usuario_logado, f'<h3>{um_pergunta_db.enunciado}</h3>')
    # Alternatives
    for alt in um_pergunta_db.alternativas['array']:
        assert_contains(reponse_com_usuario_logado, alt)


def testa_o_redireionamento_para_a_pagina_de_classificao(reponse_com_usuario_logado_alem_da_ultima_pergunta):
    '''
    Testa o redirecionamento para a pagina de classifica quando tem se acessar uma pergunta fora do limite
    '''

    assert reponse_com_usuario_logado_alem_da_ultima_pergunta.status_code == HTTPStatus.FOUND  # 302
    assert reponse_com_usuario_logado_alem_da_ultima_pergunta.headers['Location'] == reverse('base:classificacao')
