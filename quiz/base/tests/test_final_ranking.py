import pytest
# from http import HTTPStatus

from django.test import Client
from django.urls import reverse

# from quiz.base.django_assertions import assert_contains


@pytest.fixture
def response(client: Client):
    return client.get(reverse('base:classificacao'))


def test_reverse_for_final_ranking_page():
    assert '/classificacao/' == reverse('base:classificacao')


# def test_final_ranking_page_status_ok(response):
#     assert response.status_code == HTTPStatus.OK  # 200


# def test_final_ranking_page_content(response):
#     assert_contains(response, '<h3>Ranking</h3>')
