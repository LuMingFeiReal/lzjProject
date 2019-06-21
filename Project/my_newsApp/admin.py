from django.contrib import admin
from .models import NewsCategory, NewsInfo
from my_commentApp.models import NewsInfoComment

# Register your models here.

# 实时新闻
class NewsInfoInline(admin.TabularInline):
    model = NewsInfoComment

# 自定义
@admin.register(NewsInfo)
class NewsInfoAdmin(admin.ModelAdmin):
    # def cate(self):
    #     return self.category
    # cate.short_description = '类型'

    # 列表页属性
    list_display = ['title', 'author_name', 'date', 'category']  # 展示列
    list_filter = ['category']  # 过滤字段
    list_per_page = 50    # 分页
    search_fields = ['title']    # 按什么搜索

    # 添加、修改页属性
    # fields = []   # 需要修改添加的属性
    # fieldsets = []    # 给属性分组 不能与fields共同使用
    inlines = [NewsInfoInline]

