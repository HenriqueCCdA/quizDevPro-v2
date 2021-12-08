import pytest
from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains


@pytest.fixture
def response_sem_usuario_logado(client: Client, uma_pergunta_db, uma_reposta_db):
    return client.get(reverse('base:classificacao'))


@pytest.fixture
def response_com_usuario_logado(client_login_simpliciado: Client, uma_pergunta_db, uma_reposta_db):
    '''
    Cliente com um usuario logado com apenas um pergunta ativa. Este cliente acesse uma pergunta existente
    :param client_login_simpliciado:
    :param um_pergunta_db:
    :return: response
    '''
    return client_login_simpliciado.get(reverse('base:classificacao'))


def test_reverse_para_a_pagina_de_classificacao():
    assert '/classificacao/' == reverse('base:classificacao')


def test_redirecionamento_da_pagina_de_classificacao_sem_usuario_logado(response_sem_usuario_logado):
    '''
    Testa o redirecionamento da pagina de classificacao quando o usuario não esta logado
    '''
    assert response_sem_usuario_logado.status_code == HTTPStatus.FOUND  # 302
    assert response_sem_usuario_logado.headers['Location'] == reverse('base:home')


def test_status_da_pagina_de_classificacao_com_usuario_logado(response_com_usuario_logado):
    '''
    Testa o estatus da pagina de classificacao quando o usuario esta logado
    '''
    assert response_com_usuario_logado.status_code == HTTPStatus.OK  # 200


def test_conteudo_da_pagina_de_classificacao_com_usuario_logado(response_com_usuario_logado):
    '''
    Testa o conteudo da pagina classificacao
    '''
    assert_contains(response_com_usuario_logado, '<h3>Ranking</h3>')
