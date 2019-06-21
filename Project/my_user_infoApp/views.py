import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from my_articleApp.views import get_article, NewsArticle
from my_newsApp.views import get_news
from my_toolsApp.toolsPublic import page_list,get_category_ch

# Create your views here.

@login_required
def personal(request):
    return render(request, 'personal.html')



# 更新用户个人信息
@login_required
def update_info(request):
    msg = ''
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('nickname')
        age = request.POST.get('age')
        birth = request.POST.get('birthday')
        sex = request.POST.get('sex')
        mail = request.POST.get('email')

        user.newsuser.nickname = name
        user.newsuser.age = age
        user.newsuser.sex = sex
        user.newsuser.birthday = birth
        user.email = mail
        user.newsuser.save()
        user.save()
        msg = settings.SUCCESS
    else:
        pass

    return HttpResponse(msg)


# 查询浏览历史记录
def get_history(request):
    user = request.user
    history = {'list':[]}
    dict_history = json.loads(user.newsuser.json_history)

    for x in dict_history['list']:
        try:
            one_history = {}
            one_history['key'] = x['key']
            if len(one_history['key']) == 20:
                one_article = get_article(x['key'])
                one_history['title'] = one_article.title
                one_history['author'] = one_article.user_key.newsuser.nickname
                if one_article.is_good:
                    one_history['category'] = '红名单'
                else:
                    one_history['category'] = '黑名单'
            else:
                one_news = get_news(x['key'])
                one_history['title'] = one_news.title
                one_history['author'] = one_news.author_name
                one_history['category'] = one_news.category.category_ch
            one_history['time'] = x['time']
            history['list'].append(one_history)

        except ObjectDoesNotExist:
            dict_history['list'].remove(x)
            dict_history['count'] = dict_history['count'] - 1
            temp = user.newsuser
            temp.json_history = json.dumps(dict_history, ensure_ascii = False)
            temp.save()

    history_page = {}
    if history['list']:
        history_page = page_list(history['list'], 13)
    else:
        history_page['page_num'] = 0

    return JsonResponse(history_page, json_dumps_params={'ensure_ascii':False})



# 查询发表文章
def get_all_articles(request):
    user = request.user
    articles = NewsArticle.objects.filter(user_key = user)
    result = []
    for one in articles:
        temp = {}
        temp['key'] = one.uniquekey
        temp['title'] = one.title
        temp['author'] = one.user_key.username
        if one.is_good:
            temp['category'] = '红名单'
        else:
            temp['category'] = '黑名单'
        temp['time'] = str(one.create_date)
        if one.is_checked:
            temp['ischecked'] = '通过'
        else:
            temp['ischecked'] = '待审核'
        result.append(temp)

    article_page = {}
    if result:
        article_page = page_list(result, 13)
    else:
        article_page['page_num'] = 0

    return JsonResponse(article_page, json_dumps_params={'ensure_ascii':False})


# 文章审核列表
def get_article_check(request):
    articles = NewsArticle.objects.filter(is_checked = False)
    result = []
    for one in articles:
        temp = {}
        temp['key'] = one.uniquekey
        temp['title'] = one.title
        temp['author'] = one.user_key.username
        if one.is_good:
            temp['category'] = '红名单'
        else:
            temp['category'] = '黑名单'
        temp['time'] = str(one.create_date)
        if one.is_checked:
            temp['ischecked'] = '通过'
        else:
            temp['ischecked'] = '待审核'
        result.append(temp)

    check_page = {}
    if result:
        check_page = page_list(result, 13)
    else:
        check_page['page_num'] = 0

    return JsonResponse(check_page, json_dumps_params={'ensure_ascii':False})

# 审核通过
def pass_check(request):
    key = request.POST.get('key')
    article = NewsArticle.objects.get(uniquekey = key)
    article.is_checked = True
    article.save()

    return HttpResponse(settings.SUCCESS)


# 获取兴趣json生成charts
def get_interest(request):
    user = request.user
    json_i = {}
    json_i['list'] = json.loads(user.newsuser.interest)
    json_i['cates'] = get_category_ch()
    if user.newsuser.i_keywords:
        json_i['keywords'] = user.newsuser.i_keywords.split('$')
    # print(json.dumps(json_i, indent=4))

    return JsonResponse(json_i, json_dumps_params={'ensure_ascii':False})



# 修改密码
@login_required
def change_password(request):
    user = request.user
    old_pwd = request.POST.get('old_password')
    pwd = request.POST.get('password')
    repwd = request.POST.get('repassword')

    msg = ''
    if pwd == repwd:
        if user.check_password(old_pwd):
            user.set_password(pwd)
            user.save()
            auth.logout(request)
            msg = settings.SUCCESS
        else:
            msg = settings.ERROR_PASSWORD
    else:
        msg = settings.DIFFERENT_PASSWORD

    return HttpResponse(msg)
