import itertools
import json
import operator
import random
import time

from django.conf import settings
from django.shortcuts import render
from django.db.models import Q

from my_toolsApp.toolsPublic import get_weather_by_ip, get_now, random_news
from my_articleApp.models import NewsArticle

from .models import NewsInfo


# **************************************************************
# 获取新闻
def get_news(key):
    return NewsInfo.objects.get(pk = key)

# 获取指定类别新闻
def get_news_by_category(category_py, first = 0, last = 20):
    return NewsInfo.objects.filter(
        category__category_py = category_py
    )[first:last]


# 获取指定类别随机新闻
def get_random_news(category_py, num = 5):
    news_list = get_news_by_category(category_py, first = 0, last = 100)
    result = random_news(news_list, total = num)

    return result


# 判断是否存在历史记录
def exist_history(user, key):
    flag = False
    sql_history = json.loads(user.newsuser.json_history)
    for x in sql_history['list']:
        if x['key'] == key:
            sql_history['list'].remove(x)
            flag = True
    r = {}
    r['flag'] = flag
    r['sql_history'] = sql_history

    return r


# 更新历史记录
def update_history(user, key, sql_history):
    now = get_now()
    history = {'key': key,'time': now}
    sql_history['list'].insert(0, history)
    sql_history['count'] = len(sql_history['list'])
    new_history = json.dumps(sql_history, ensure_ascii = False)
    user.newsuser.json_history = new_history

    return user

# 更新用户类别偏向
def update_interest(user, cate_id):
    sql_interest = json.loads(user.newsuser.interest)
    one = sql_interest[cate_id - 1]
    one['value'] = one['value'] + 1
    # new_interest = json.dumps(dict(sorted(\
    #     sql_interest.items(),key = lambda x:x[1],reverse = True)), ensure_ascii=False)
    new_interest = json.dumps(sql_interest, ensure_ascii=False)

    user.newsuser.interest = new_interest

    return user

# 最近访问新闻关键词
def update_keywords(user, news_keywords):
    news_keywords_list = news_keywords.split('$')
    sql_i_keywords = user.newsuser.i_keywords
    needs = []
    needs.extend(news_keywords_list[0:2])

    new_i_keywords = ''
    if sql_i_keywords:
        sql_i_keywords_list = sql_i_keywords.split('$')
        for x in needs:
            if x in sql_i_keywords_list:
                sql_i_keywords_list.remove(x)
        needs.extend(sql_i_keywords_list)
        new_i_keywords = '$'.join(needs[0:10])
    else:
        new_i_keywords = '$'.join(needs)

    user.newsuser.i_keywords = new_i_keywords

    return user

# 通过关键词查找类似新闻
def get_news_by_keywords(keywords):
    keywords = keywords.split('$')
    r = NewsInfo.objects.filter(Q(keywords__icontains = keywords[0]),\
        Q(keywords__icontains = keywords[1]))
    print(r)
    return r


# 相似新闻
def similar_news_list(ikeywords, total):
    i_keywords_list = ikeywords.split('$')
    news_list = NewsInfo.objects.all()
    R = []
    for one in news_list:
        temp = {}
        temp['news'] = one
        temp['same'] = len([x for x in i_keywords_list if x in one.keywords])
        R.append(temp)
    sorted_x = sorted(R, key=operator.itemgetter('same'), reverse=True)[0:50]
    n_list = []
    for one in sorted_x:
        n_list.append(one['news'])
    result = random_news(n_list, total = total)

    return result


# **************************************************************

# Create your views here.
def home(request):
    # news_type = ['top','shehui','guonei','guoji','yule','tiyu','junshi'\
    # \,'keji','caijing','shishang']
    news_types = ['shehui', 'guoji', 'yule', 'tiyu', 'junshi', 'keji', 'caijing', 'shishang']
    news_yaowen = get_news_by_category('guoji', 0, 6)
    for news_type in news_types:
        news_yaowen = itertools.chain(
            news_yaowen,
            get_news_by_category(news_type, 0, 2)
        )

    news_top = get_news_by_category('top', 0, 15)
    news_tiyu = get_news_by_category('tiyu', 0, 3)

    # 新闻推荐及视觉焦点
    news_other = {
        'news_pic': get_news_by_category('keji', 0, 6),
        'news_recommend': get_news_by_category('shishang', 0, 16)
    }

    if request.user.is_authenticated and request.user.newsuser.i_keywords:
        i_keywords = request.user.newsuser.i_keywords
        # print(similar_news_list(i_keywords, 16))
        news_other['news_recommend'] = similar_news_list(i_keywords, 16)

    news_types = ['shehui', 'guoji', 'yule', 'tiyu', 'junshi']
    news_down = []
    news_down.append(get_news_by_category('guonei', 4, 14))
    for news_type in news_types:
        news_down.append(get_news_by_category(news_type, 2, 12))

    news_types = ['keji', 'caijing', 'shishang']
    news_down2 = []
    for news_type in news_types:
        news_down2.append(get_news_by_category(news_type, 2, 12))


    # 用户的文章
    article_red = NewsArticle.objects.filter(is_good = 1, is_checked = True)[0:6]
    article_black = NewsArticle.objects.filter(is_good = 0, is_checked = True)[0:9]


    # 天气情况
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    ip = '223.67.189.61'
    weather = get_weather_by_ip(ip)
    weather_json = json.loads(weather.weather_info)
    # print(weather_json)
    return render(request, 'home.html',{
        'news_yaowen': news_yaowen,
        'news_top':news_top, 'news_tiyu':news_tiyu,
        'news_other':news_other,
        'news_down': news_down,
        'news_down2':news_down2,
        'red':article_red,
        'black':article_black,
        'weather':weather_json
    })


def kind(request, cate_req):
    # 打印请求来源
    # if 'HTTP_REFERER' in request.META:
    #     print(request.META['HTTP_REFERER'])
    cate_t = {'top':'头条' , 'shehui':'社会', 'guonei':'国内', 'guoji':'国际', \
        'yule':'娱乐', 'tiyu':'体育', 'junshi':'军事', 'keji':'科技', 'caijing':'财经', 'shishang':'时尚'}
    news_indicators = get_news_by_category(cate_req, 0, 3)
    news_top = get_news_by_category(cate_req, 3, 5)
    news_main = get_news_by_category(cate_req, 5, 25)
    # 需要重写
    news_others = []
    news_others.append(get_random_news(category_py = cate_req, num = 5))
    news_others.append(get_random_news(category_py = cate_req, num = 5))

    return render(request, 'kind.html', {
        'cate_req':[cate_req, cate_t[cate_req]],
        'news_top': news_top,
        'news_indicators': news_indicators,
        'news_main': news_main,
        'news_others':news_others
    })

# is_anonymous()
# 是否是匿名用户。
# is_authenticated()
# 用户是否通过验证，登陆。
# UPDATE news_user SET history = "{\"count\": 0, \"list\": []}"
def detail(request, key):
    news = ''
    types = ''
    cate_id = ''
    # ----------------------------用户文章--------------------------------
    if len(key) == 20:
        types = 'article'
        news = NewsArticle.objects.get(pk = key)
        # 需要重写
        related_news = get_news_by_category('shehui', 0, 6)
        comments = news.articlecomments.all()
    # -------------------------------------------------------------------
    else:
        news = NewsInfo.objects.get(pk = key)
        cate_id = news.category.id
        comments = news.newscomments.all()
        related_news = similar_news_list(news.keywords, 6)
    # 存放用户历史记录
    user = request.user
    if user.is_authenticated:   # 验证用户登陆
        # 历史记录
        temp = exist_history(user, key)
        user = update_history(user, key ,temp['sql_history'])
        # -----------------------
        # ----------------------------兴趣偏向--------------------------------
        if cate_id:
            # 用户浏览的类别偏向
            if not temp['flag']:
                user = update_interest(user, cate_id)
            # --------------------------
            # 最近访问新闻关键词
            user = update_keywords(user, news.keywords)
            # get_news_by_keywords(news.keywords)
            #---------------------------
        else:
            pass
        # -------------------------------------------------------------------
        user.newsuser.save()
    else:
        pass

    return render(request, 'detail.html',{
        'main': news,
        'related_news': related_news,
        'type': types,
        'comments': comments
    })



# 搜索结果
def search(request):
    keyword = request.GET.get('keyword')
    s_result = NewsInfo.objects.filter(Q(title__icontains = keyword))
    count = len(s_result)

    return render(request, 'search.html', {
        'count': count,
        'result': s_result,
        'keyword':keyword
    })


def keyword_search(request):
    keyword = request.GET.get('keyword')
    s_result = NewsInfo.objects.filter(Q(keywords__icontains = keyword))
    count = len(s_result)

    return render(request, 'search.html', {
        'count': count,
        'result': s_result,
        'keyword':keyword
    })



def test(request):
    # ip = ''
    # if 'HTTP_X_FORWARDED_FOR' in request.META:
    #     ip =  request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
    # print(request.META['HTTP_USER_AGENT'])


    return render(request, 'test.html')
