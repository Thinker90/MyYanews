import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_home_page(client, news):
    for i in range(11):
        news
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.context['object_list']) <= 10
    news_list = response.context['object_list']
    dates = [news.date for news in news_list]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_home_page(client, id_news, comment, news):
    for i in range(2):
        comment
    url = reverse('news:detail', args=id_news)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    news = response.context['news']
    dates = [comment.created for comment in news.comment_set.all()]
    assert dates == sorted(dates, reverse=True)
    assert 'form' not in response.context
