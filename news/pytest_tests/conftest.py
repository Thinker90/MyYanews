import pytest
from datetime import timedelta
from django.conf import settings
from django.test import Client
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news_list(author, client):
    return [
        News(title=f'Новость {index}',
             text='Просто текст.',
             date=timezone.now() - timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]


@pytest.fixture
def news(author, client):
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=timezone.now(),
    )


@pytest.fixture
def comment(author, client, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст новости',
        created=timezone.now(),
    )


@pytest.fixture
def id_news(news):
    return (news.id,)


@pytest.fixture
def id_comment(comment):
    return (comment.id,)
