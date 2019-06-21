from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from my_articleApp.views import get_article
from my_newsApp.views import get_news

from .models import NewsArticleComment, NewsInfoComment

# Create your views here.


def add_article_comment(article, user, content, date):
    NewsArticleComment.objects.create(
        article_key = article,
        user_key = user,
        content = content,
        date = date
    )


def add_news_comment(news, user, content, date):
    NewsInfoComment.objects.create(
        news_key = news,
        user_key = user,
        content = content,
        date = date
    )


def add_comment(request):
    uniquekey = request.POST.get('uniquekey')
    flag = request.POST.get('flag')
    content = request.POST.get('content')
    now = request.POST.get('date')
    user = request.user

    if flag:
        news = get_news(uniquekey)
        add_news_comment(news, user, content, now)
    else:
        article = get_article(uniquekey)
        add_article_comment(article, user, content, now)

    return HttpResponse('ok')

