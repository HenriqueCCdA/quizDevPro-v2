import pytest
from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains


@pytest.fixture
def response(client: Client):
    return client.get(reverse('base:pergunta', kwargs={'slug': 1}))


@pytest.mark.parametrize(('slug', ), [
    (1, ),
    (2, ),
])
def test_reverse_for_question_page(slug):
    assert f'/pergunta/{slug}' == reverse('base:pergunta', kwargs={'slug': slug})


def test_question_page_status_ok(response):
    assert response.status_code == HTTPStatus.OK  # 200


def test_home_content(response):
    assert_contains(response, '<h2>Questão')
