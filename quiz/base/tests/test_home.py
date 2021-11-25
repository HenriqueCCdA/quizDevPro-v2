
import pytest
from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains


@pytest.fixture
def response(client: Client):
    return client.get(reverse('base:home'))


def test_home_status_ok(response):
    assert response.status_code == HTTPStatus.OK  # 200


def test_home_content(response):
    assert_contains(response, '<button>Entrar</button>')
