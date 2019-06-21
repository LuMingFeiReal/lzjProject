from django.contrib import admin
from .models import NewsArticle
from my_commentApp.models import NewsArticleComment

# Register your models here.
# 用户文章
class NewsArticleInline(admin.TabularInline):
    model = NewsArticleComment

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_key', 'create_date']  # 展示列
    list_filter = ['is_good']  # 过滤字段
    list_per_page = 50    # 分页
    search_fields = ['title']    # 按什么搜索

    inlines = [NewsArticleInline]

