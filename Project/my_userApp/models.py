from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from my_toolsApp.toolsPublic import create_interest

# Create your models here.
class NewsUser(models.Model):
    TYPE_CHOICES = (
        (0, '女'),
        (1, '男')
    )

    uid = models.OneToOneField(User, models.CASCADE, db_column='uid', primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=255, blank=True, null=True)
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    sex = models.IntegerField(verbose_name='性别', blank=True, null=True, choices=TYPE_CHOICES)
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    json_history = models.TextField(blank=True, null=True)
    interest = models.TextField(blank=True, null=True)
    i_keywords = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def create_newsuser(cls, user ,nickname):
        user = cls(uid = user, nickname = nickname ,age = 0, sex = 0,\
            json_history = '{"count": 0, "list": []}', interest = create_interest())
        user.save()
        return True

    def sex_name(self):
        name = ''
        if self.sex:
            name = '男'
        else:
            name = '女'
        return name
    sex_name.short_description = '性别'

    def user_email(self):
        return self.uid.email
    user_email.short_description = '邮箱'


    # 元组
    class Meta:
        managed = False
        db_table = 'news_user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


    # 重写输出
    def __str__(self):
        return self.uid.username


# 删除后操作
@receiver(post_delete, sender = NewsUser)
def after_userinfo_delete(instance, **kwargs):
    print(kwargs)
    user = instance.uid
    user.delete()



@receiver(post_save, sender = User)
def after_user_create(instance, created, **kwargs):
    print(kwargs)
    if created:
        # 在用户注册后创建自己的用户字段
        NewsUser.create_newsuser(user = instance, nickname = instance.username)



