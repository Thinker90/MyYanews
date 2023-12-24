import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, url_args',
    (
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture('id_news'))
    )
)
def test_home_availability_for_anonymous_user(client, name, url_args):
    if url_args is not None:
        url = reverse(name, args=url_args)
    else:
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_pages_availability_for_different_users(
        parametrized_client, name, id_comment, expected_status
):
    url = reverse(name, args=id_comment)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, comment_object',
    (
            ('news:edit', pytest.lazy_fixture('id_comment')),
            ('news:delete', pytest.lazy_fixture('id_comment')),
    ),
)
def test_redirects(client, name, comment_object):
    login_url = reverse('users:login')
    url = reverse(name, args=comment_object)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
