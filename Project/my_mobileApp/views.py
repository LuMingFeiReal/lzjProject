from django.shortcuts import render
from django.http import JsonResponse
from my_newsApp.views import NewsInfo,get_news_by_category,get_news
from my_toolsApp.toolsPublic import get_weather_by_ip
import itertools
import json


def news_to_array(news_out):
    news_array = []
    for one in news_out:
        temp = {}
        temp['name'] = one.author_name
        temp['title'] = one.title
        temp['pic'] = one.thumbnail_pic
        temp['url'] = one.uniquekey
        news_array.append(temp)
    return news_array


# Create your views here.
def mhome(request):
    news_top = get_news_by_category('guoji', 0, 2)

    ip = 0
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    ip = '223.67.189.61'

    weather = get_weather_by_ip(ip)
    weather_json = json.loads(weather.weather_info)

    return render(request, 'mobile/mhome.html',{
        'news_top':news_top,
        'weather':weather_json
    })


def mkind(request, cate_req):
    news_car = get_news_by_category(cate_req, 0, 5)
    news_top = get_news_by_category(cate_req, 5, 7)

    return render(request, 'mobile/mkind.html', {
        'news_car':news_car,
        'news_top':news_top
    })

def mdetail(request, unkey):
    main = get_news(unkey)
    bottom_top = get_news_by_category(main.category.category_py, 0, 3)
    return render(request, 'mobile/mdetail.html',{
        'main':main,
        'bottom_top':bottom_top
    })


def get_home_news(request):
    str_num = request.GET.get('pagenum')
    num = 0
    if str_num:
        num = int(str_num)
    news_json = {}

    news_up = get_news_by_category('top', 0, 5)
    news_top = news_to_array(news_up)

    news_list = NewsInfo.objects.all()[20*num:20*(num+1)]
    news_ul = news_to_array(news_list)

    news_json['news_top'] = news_top
    news_json['news_ul'] = news_ul

    return JsonResponse(
        news_json,
        json_dumps_params={'ensure_ascii':False}
    )


def get_kind_news(request):
    cate = request.GET.get('cate')
    str_num = request.GET.get('pagenum')
    num = 0
    if str_num:
        num = int(str_num)

    news_json = {}
    news_list = get_news_by_category(cate, 20*num+7, 20*(num+1)+7)
    news_ul = news_to_array(news_list)

    news_json['news_ul'] = news_ul

    return JsonResponse(
        news_json,
        json_dumps_params={'ensure_ascii':False}
    )
