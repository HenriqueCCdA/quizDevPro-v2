import pytest
from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains


INDICE = 1


@pytest.fixture
def response_sem_usuario_logado(client: Client, uma_pergunta_db):
    return client.get(reverse('base:pergunta', kwargs={'indice': INDICE}))


@pytest.fixture
def response_com_usuario_logado(client_login_simpliciado: Client, uma_pergunta_db):
    '''
    Cliente com um usuario logado com apenas um pergunta ativa. Este cliente acesse uma pergunta existente
    :param client_login_simpliciado:
    :param um_pergunta_db:
    :return: response
    '''
    return client_login_simpliciado.get(reverse('base:pergunta', kwargs={'indice': INDICE}))


@pytest.fixture
def response_com_usuario_logado_alem_da_ultima_pergunta(client_login_simpliciado: Client, uma_pergunta_db):
    '''
    Cliente com um usuario logado com apenas um pergunta ativa. Este cliente acesse uma pergunta não existente
    :param client_login_simpliciado:
    :param um_pergunta_db:
    :return: reponse
    '''
    return client_login_simpliciado.get(reverse('base:pergunta', kwargs={'indice': INDICE + 1}))


@pytest.mark.parametrize(('indice', ), [
    (1, ),
    (2, ),
])
def testa_reverse_para_a_pagina_de_pergunta(indice):
    '''
    Testa a funcao reverse para pergunta
    :param slug:
    '''
    assert f'/pergunta/{indice}' == reverse('base:pergunta', kwargs={'indice': indice})


def testa_status_code_pagina_da_pergunta_sem_o_usuario_logado(response_sem_usuario_logado, db):
    '''
    Testa o redirecionamento da pagina da pergunta quando o usuario não esta logado
    '''
    assert response_sem_usuario_logado.status_code == HTTPStatus.FOUND  # 302
    assert response_sem_usuario_logado.headers['Location'] == reverse('base:home')


def testa_status_code_pagina_da_pergunta_com_o_usuario_logado(response_com_usuario_logado):
    '''
    Testa o redirecionamento da pagina da pergunta quando o usuario não esta logado
    '''

    assert response_com_usuario_logado.status_code == HTTPStatus.OK  # 200


def testa_o_conteudo_pagina_da_pergunta_com_o_usuario_logado(response_com_usuario_logado, uma_pergunta_db):
    '''
    Testa o contuedo da paragina da pergunta com o usuario o usuario logado.
    '''
    indice = INDICE

    assert_contains(response_com_usuario_logado, f'<h2> Questão {indice} </h2>')
    assert_contains(response_com_usuario_logado, f'<h3>{uma_pergunta_db.enunciado}</h3>')
    # Alternatives
    for alt in uma_pergunta_db.alternativas['array']:
        assert_contains(response_com_usuario_logado, alt)


def testa_o_redireionamento_para_a_pagina_de_classificao(response_com_usuario_logado_alem_da_ultima_pergunta):
    '''
    Testa o redirecionamento para a pagina de classifica quando tem se acessar uma pergunta fora do limite
    '''

    assert response_com_usuario_logado_alem_da_ultima_pergunta.status_code == HTTPStatus.FOUND  # 302
    assert response_com_usuario_logado_alem_da_ultima_pergunta.headers['Location'] == reverse('base:classificacao')
