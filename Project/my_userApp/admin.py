from django.contrib import admin
from .models import NewsUser
from django.contrib.auth.models import User
# Register your models here.

@admin.register(NewsUser)
class NewsUserAdmin(admin.ModelAdmin):
    ordering = ('uid',) # 排序
    list_display = ['uid', 'nickname', 'sex_name', 'age', 'user_email', 'birthday']  # 展示列
    list_per_page = 50    # 分页
    search_fields = ['uid__username']    # 按什么搜索

    # 设置可编辑字段
    # list_editable = ['nickname', 'age', 'birthday']
