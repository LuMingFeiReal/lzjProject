import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.
class NewsArticle(models.Model):
    uniquekey = models.CharField(primary_key=True, max_length=255)
    user_key = models.ForeignKey(
        User, models.DO_NOTHING,
        db_column='user_key',
        blank=True,
        null=True
    )
    is_good = models.BooleanField()
    title = models.CharField(max_length=255, blank=True, null=True)
    first_p = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)
    pic_list = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'news_article'
        ordering = ['-create_date']
        verbose_name = '文章信息'
        verbose_name_plural = '文章信息'



# 删除前的操作
@receiver(pre_delete, sender = NewsArticle)
def pre_article_delete(instance, **kwargs):
    # 未用到的变量============
    print(kwargs)
    # =======================
    pic_list = instance.pic_list.split('&')
    for one in pic_list:
        path = '%s%s' %(settings.BASE_DIR, one)
        path = path.replace('/static/', '/common_static/')
        print(path)
        os.remove(path) # 删除文件
