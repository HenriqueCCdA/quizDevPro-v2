from http import HTTPStatus

from django.test import Client


def test_home_stattus_ok(client: Client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK # 200
