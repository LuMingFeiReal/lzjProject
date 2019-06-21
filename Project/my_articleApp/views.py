import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from my_toolsApp.toolsPublic import random_code, uploadImg, page_list

from .models import NewsArticle


# Create your views here.
def get_article(key):
    return NewsArticle.objects.get(pk = key)

# 添加文章页面
def add_page(request):
    return render(request, 'addpage.html')


# 文本转为html
def text_to_html(text):
    html = ''
    start_p = '<p>'
    end_p = '</p>'
    for one in text.split('\r\n'):
        if one != '':
            html += (start_p + one + end_p)
    return html


# 图片转为html
def img_to_html(url):
    html = '<p class="a_pic"><img src="' + url + '" ></p>'
    return html


# 添加文章
def add_article(request):
    result = ''
    if request.method == 'POST' and request.user.is_authenticated:
        x = request.POST.get('type').split(',')
        html = ''
        first_p = ''
        pic_list = []
        for i, j in enumerate(x):
            string = 'name' + str(i)
            if j == 'pic' and request.FILES.get(string):
                # 可接收的文件类型
                can_rec = ['PNG', 'JPG', 'JPEG']
                picf = request.FILES.get(string)
                ftype = picf.name.split('.')[-1].upper()
                if ftype in can_rec:
                    # 保存图片并返回地址
                    url = uploadImg(picf)
                    html += img_to_html(url)
                    pic_list.append(url)
                else:
                    result = '反正就是有错'
                    break
            else:
                if i == 0:
                    first_p = request.POST.get(string)
                html += text_to_html(request.POST.get(string))
        is_good = request.POST.get('article_type')

        NewsArticle.objects.create(uniquekey = random_code(20), user_key = request.user, \
            is_good = is_good, title = request.POST.get('title'), first_p = first_p, html = html, \
                pic = pic_list[0], pic_list = "&".join(pic_list), create_date = datetime.now())
        # 成功保存文章
        result = settings.SUCCESS
    else:
        result = settings.ILLEGAL_REQUEST

    return HttpResponse(result)

# 曝光墙
def wall(request):
    red = NewsArticle.objects.filter(is_good = True, is_checked = True)
    black = NewsArticle.objects.filter(is_good = False, is_checked = True)
    return render(request, 'wall.html', {"red": red, "black":black})


# 删除文章
def remove_article(request):
    key = request.GET.get('uniquekey')
    article = get_article(key)
    article.delete()

    return HttpResponse('ok')




