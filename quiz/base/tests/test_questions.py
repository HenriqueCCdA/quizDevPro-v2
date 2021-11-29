import pytest
from http import HTTPStatus
from model_bakery import baker

from django.test import Client
from django.urls import reverse

from quiz.base.django_assertions import assert_contains
from quiz.base.models import Pergunta


SLUG = 1


@pytest.fixture
def one_question(db):
    alternatives = ['def', 'func', '@', 'if']
    return baker.make(Pergunta, disponivel=True, alternativas={'array': alternatives})


@pytest.fixture
def response(client: Client, db):
    return client.get(reverse('base:pergunta', kwargs={'slug': SLUG}))


@pytest.fixture
def response_with_question(client: Client, one_question):
    return client.get(reverse('base:pergunta', kwargs={'slug': 1}))


@pytest.mark.parametrize(('slug', ), [
    (1, ),
    (2, ),
])
def test_reverse_for_question_page(slug):
    '''
    Test reverse functio for pergunta for the slugs 1 and 2
    :param slug:
    '''
    assert f'/pergunta/{slug}' == reverse('base:pergunta', kwargs={'slug': slug})


def test_question_page_status_ok(response):
    '''
    Test the status code of question page
    :param response:
    '''
    assert response.status_code == HTTPStatus.OK  # 200


def test_question_page_content_with_question(response_with_question, one_question):
    '''
    Test if the question is correct rendering in de page.

    :param response:
    :param one_question:
    '''
    slug = SLUG

    assert_contains(response_with_question, f'<h2> Questão {slug} </h2>')
    assert_contains(response_with_question, f'<h3>{one_question.enunciado}</h3>')
    # Alternatives
    for alt in one_question.alternativas['array']:
        assert_contains(response_with_question, f'<p class="choice-text">{alt}</p>')
