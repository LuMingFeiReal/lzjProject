from django.contrib.auth.models import User
from django.db import models

from my_articleApp.models import NewsArticle
from my_newsApp.models import NewsInfo


# Create your models here.
class NewsInfoComment(models.Model):
    news_key = models.ForeignKey(
        NewsInfo,
        models.CASCADE,
        db_column = 'news_key',
        blank = True,
        null = True,
        related_name = "newscomments"
    )
    user_key = models.ForeignKey(
        User,
        models.CASCADE,
        db_column = 'user_key',
        blank = True,
        null = True
    )
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_info_comment'
        ordering = ['-date']


class NewsArticleComment(models.Model):
    article_key = models.ForeignKey(
        NewsArticle,
        models.CASCADE,
        db_column = 'article_key',
        blank = True,
        null = True,
        related_name = "articlecomments"
    )
    user_key = models.ForeignKey(
        User,
        models.CASCADE,
        db_column = 'user_key',
        blank = True,
        null = True
    )
    content = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_article_comment'
        ordering = ['-date']
