import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects

@pytest.mark.parametrize(
    'name',  # Имя параметра функции
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_home_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK