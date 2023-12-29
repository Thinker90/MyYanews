import pytest
from django.urls import reverse
from http import HTTPStatus

from news.models import Comment, News


@pytest.mark.django_db
def test_home_page(client, news_list):
    News.objects.bulk_create(news_list)
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert (response.context['object_list']).count() <= 10


@pytest.mark.django_db
def test_sorted_obj(client):
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['object_list']
    dates = [news.date for news in news_list]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_comment_detail_page(client, id_news, comment):
    url = reverse('news:detail', args=id_news)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    news = response.context['news']
    dates = [comment.created for comment in news.comment_set.all()]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_context_form(client, id_news):
    url = reverse('news:detail', args=id_news)
    response = client.get(url)
    assert 'form' not in response.context
