import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse
from http import HTTPStatus

from news.models import News, Comment
from news.forms import WARNING, BAD_WORDS

FORM_DATA = {'text': 'Новый текст', }


def test_user_can_create_comment(author_client, author, id_news):
    comment_before = Comment.objects.count()
    url = reverse('news:detail', args=id_news)
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == comment_before + 1
    new_comment = Comment.objects.last()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, id_news):
    comment_before = Comment.objects.count()
    url = reverse('news:detail', args=id_news)
    response = client.post(url, data=FORM_DATA)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comment_before


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, id_comment, id_news):
    url = reverse('news:edit', args=id_comment)
    url_redirect = reverse('news:detail', args=id_news)
    comment = Comment.objects.get(pk=id_comment[0])
    response = author_client.post(url, FORM_DATA)
    assertRedirects(response, url_redirect + '#comments')
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, id_comment, id_news):
    comment_before = Comment.objects.count()
    url = reverse('news:delete', args=id_comment)
    url_redirect = reverse('news:detail', args=id_news)
    response = author_client.post(url)
    assertRedirects(response, url_redirect + '#comments')
    assert Comment.objects.count() == comment_before-1


def test_other_user_cant_delete_comment(admin_client, id_comment):
    comment_before = Comment.objects.count()
    url = reverse('news:delete', args=id_comment)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comment_before


def test_bad_text_comment(author_client, id_news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=id_news)
    comment_before = Comment.objects.count()
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == comment_before
