from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewsCategory(models.Model):
    category_ch = models.CharField(max_length=255, blank=True, null=True)
    category_py = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_category'
        verbose_name = '类型'
        verbose_name_plural = '类型'

    def __str__(self):
        return self.category_ch



class NewsInfo(models.Model):
    uniquekey = models.CharField(primary_key=True, max_length=255)
    author_name = models.CharField(verbose_name='作者', max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        NewsCategory,
        models.DO_NOTHING,
        db_column = 'category',
        blank = True,
        null = True
    )
    date = models.DateTimeField(verbose_name='日期', blank=True, null=True)
    title = models.CharField(verbose_name='标题', max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_num = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_pic = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        verbose_name = '新闻信息'
        verbose_name_plural = '新闻信息'
        db_table = 'news_info'
        ordering = ['-date']

    def __str__(self):
        return self.title







