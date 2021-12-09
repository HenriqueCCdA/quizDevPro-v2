import pytest
from http import HTTPStatus
from model_bakery import baker

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains
from quiz.base.models import Aluno


@pytest.fixture
def response_get(client: Client):
    return client.get(reverse('base:home'))


@pytest.fixture
def response_post_com_aluno_com_email_cadastrado(client: Client, db, um_aluno_db):
    dct = {'email': um_aluno_db.email,
           'nome': um_aluno_db.nome}
    return client.post(reverse('base:home'), dct)


@pytest.fixture
def aluno_novo():
    return baker.prepare(Aluno)


@pytest.fixture
def response_post_com_aluno_com_email_novo(client: Client, aluno_novo, db):
    dct = {'nome': aluno_novo.nome,
           'email': aluno_novo.email}
    return client.post(reverse('base:home'), dct)


def test_status_code_ok(response_get):
    assert response_get.status_code == HTTPStatus.OK  # 200


def test_conteudo_home(response_get):
    assert_contains(response_get, '<form class="login-form"')


def test_home_post_com_aluno_com_email_novo(response_post_com_aluno_com_email_novo, aluno_novo):
    '''
    Testa o caso quando é um aluno com email novo. Neste caso o aluno nnovo é automaticamente
    cadastrado é a pagina é redirecionada para primeira pergunta
    '''

    aluno = Aluno.objects.get(email=aluno_novo.email)

    assert aluno_novo.nome == aluno.nome
    assert aluno_novo.email == aluno.email
    assert response_post_com_aluno_com_email_novo.status_code == HTTPStatus.FOUND
    assert response_post_com_aluno_com_email_novo.headers['Location'] == reverse('base:pergunta',  kwargs={'indice': 1})


def test_home_post_com_aluno_com_email_cadastrado(response_post_com_aluno_com_email_cadastrado, um_aluno_db):
    '''
    Testa o caso que o aluno já tem o email cadastrado
    '''

    assert response_post_com_aluno_com_email_cadastrado.status_code == HTTPStatus.FOUND
    assert response_post_com_aluno_com_email_cadastrado.headers['Location'] == reverse('base:pergunta',
                                                                                       kwargs={'indice': 1})
