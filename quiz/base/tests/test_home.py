import pytest
from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains
from quiz.base.models import Aluno


@pytest.fixture
def response(client: Client):
    return client.get(reverse('base:home'))


@pytest.fixture
def aluno():
    dct = {'nome': 'usuario', 'email': 'usuario@gmail.com'}
    return dct


@pytest.fixture
def response_post(client: Client, db, aluno):
    return client.post(reverse('base:home'), aluno)


def test_home_status_ok(response):
    assert response.status_code == HTTPStatus.OK  # 200


def test_home_content(response):
    assert_contains(response, '<form class="login-form"')


def test_home_post(response_post, aluno):

    aluno_db = Aluno.objects.get(email='usuario@gmail.com')

    assert aluno['nome'] == aluno_db.nome
    assert aluno['email'] == aluno_db.email


def test_home_post_redirect(response_post, aluno):

    assert response_post.status_code == HTTPStatus.FOUND
