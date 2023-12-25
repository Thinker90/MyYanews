import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from http import HTTPStatus
from django.urls import reverse
from pytils.translit import slugify

from news.models import News, Comment
from news.forms import WARNING, BAD_WORDS


def test_user_can_create_comment(author_client, author, form_data, id_news):
    url = reverse('news:detail', args=id_news)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, id_news):
    url = reverse('news:detail', args=id_news)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, form_data, id_comment, id_news):
    url = reverse('news:edit', args=id_comment)
    url_redirect = reverse('news:detail', args=id_news)
    comment = Comment.objects.get(pk=id_comment[0])
    response = author_client.post(url, form_data)
    assertRedirects(response, url_redirect + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']

@pytest.mark.django_db
def test_author_can_delete_comment(author_client, id_comment, id_news):
    url = reverse('news:delete', args=id_comment)
    url_redirect = reverse('news:detail', args=id_news)
    response = author_client.post(url)
    assertRedirects(response, url_redirect + '#comments')
    assert Comment.objects.count() == 0

def test_other_user_cant_delete_comment(admin_client, id_comment):
    url = reverse('news:delete', args=id_comment)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1

def test_bad_text_comment(author_client, form_data, id_news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=id_news)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0
