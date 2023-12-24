import pytest

from datetime import datetime
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author, client):
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.now(),
    )
    return news


@pytest.fixture
def comment(author, client, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст новости',
        created=datetime.now(),
    )
    return comment


@pytest.fixture
def id_news(news):
    return (news.id,)


@pytest.fixture
def id_comment(comment):
    return (comment.id,)
