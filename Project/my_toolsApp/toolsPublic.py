import io
import itertools
import json
import math
import random
import urllib.request
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageDraw, ImageFont

from my_newsApp.models import NewsCategory

from .models import NewsWeather


# 获取当前时间
def get_now():
    # now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now

# 字符串转datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


# 随机抽取新闻
def random_news(news_list, total):
    length = len(news_list)
    result = []
    if length <= total:
        result = news_list
    else:
        xlist = random.sample(range(0, length), total)
        for x in xlist:
            # print(news_list[x].date)
            result.append(news_list[x])

    # print(result)
    return result


# 生成随机码
def random_code(x):
    strs = \
        '0123456789qwertyuopasdfghijkzxcvbnmQWERTYUOPASDFGHIJKZXCVBNM'
    string = ''
    for _ in range(0, x):
        string += strs[random.randrange(0, len(strs))]
    return string


#生成验证码
def verifycode(request):
    bgcolor = (random.randrange(20, 100),random.randrange(20, 100), \
        random.randrange(20, 100))
    width = 100
    height = 35
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)

    for i in range(0, 100):
        i = i + 1 #未使用的变量i
        xy = (random.randrange(0, width), random.randrange(0 ,height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    strs = \
        '123456789qwertyupasdfghjkzxcvbnmQWERTYUPASDFGHJKZXCVBNM'

    fontcolor = []
    rand_str = ''
    for i in range(0, 4):
        rand_str += strs[random.randrange(0, len(strs))]
        fontcolor.append((255, random.randrange(0, 255), random.randrange(0, 255)))

    font = ImageFont.truetype(r'../common_static/myHTML/fonts/BRITANIC.TTF', 30)
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor[0])
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor[1])
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor[2])
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor[3])

    del draw
    request.session['verifycode'] = rand_str

    buf = io.BytesIO()
    im.save(buf, 'png')
    return buf


#验证验证码
def confirm_code(request, user_code):
    flag =  user_code.upper() == request.session['verifycode'].upper()
    return flag


# 图片上传函数
def uploadImg(img):
    imgname = random_code(20) + '.jpg'
    imgpath = '%s/upload/article_img/%s' %(settings.STATIC_ROOT, imgname)
    with open(imgpath, 'wb') as f:
        for fimg in img.chunks():
            f.write(fimg)
    path = '/static/upload/article_img/' + imgname
    return path

# 列表分页
def page_list(items, per_page):
    result = {}

    length = len(items)
    page_num = math.ceil(length / per_page)
    result['page_num'] = page_num

    for i in range(0, page_num):
        per_items = []
        last_num = (i + 1) * per_page
        if last_num > length:
            last_num = length
        for j in range(i * per_page, last_num):
            per_items.append(items[j])
        result[str(i)] = per_items

    return result

# 生成用户兴趣偏向
def create_interest():
    cates = NewsCategory.objects.all()
    r = []
    for one in cates:
        temp = {}
        temp['name'] = one.category_ch
        temp['value'] = 0
        r.append(temp)

    return json.dumps(r ,ensure_ascii=False)


# 获取所有文章类型
def get_category_ch():
    cates = NewsCategory.objects.all()
    r = []
    for one in cates:
        r.append(one.category_ch)

    return r


# api request
def api_request(ihost, ipath, iappcode, iquerys):
    host = ihost
    path = ipath
    # method = 'GET'
    appcode = iappcode
    querys = iquerys
    # bodys = {}
    url = host + path + '?' + querys

    req = urllib.request.Request(url)
    req.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib.request.urlopen(req)
    content = response.read()
    info = json.loads(content)

    return info

# 解析天气json
def load_weather_json(info):
    temp = {}
    temp['city'] = info['showapi_res_body']['cityInfo']['c5'] # 城市
    temp['province'] = info['showapi_res_body']['cityInfo']['c7'] # 省份
    temp['country'] = info['showapi_res_body']['cityInfo']['c9'] # 国家
    temp['aqi'] = info['showapi_res_body']['now']['aqi'] # 空气质量指数
    temp['quality'] = info['showapi_res_body']['now']['aqiDetail']['quality'] #空气质量
    temp['temperature'] = info['showapi_res_body']['now']['temperature'] # 温度
    temp['pic'] = info['showapi_res_body']['now']['weather_pic'] # 图片url
    temp['wea'] = info['showapi_res_body']['now']['weather'] # 天气
    temp['time'] = info['showapi_res_body']['now']['temperature_time'] # 更新时间
    temp['dampness'] = info['showapi_res_body']['now']['sd'] # 空气湿度
    temp['windd'] = info['showapi_res_body']['now']['wind_direction'] # 风向
    temp['windp'] = info['showapi_res_body']['now']['wind_power'] # 风力
    new_info = json.dumps(temp, ensure_ascii = False)

    return new_info


# 获取天气情况api
def get_weather_info(ip):
    appcode = '13840cb278b243f9a37d0b23b43d539e'
    host = 'http://saweather.market.alicloudapi.com'
    path = '/ip-to-weather'
    querys = 'ip=' + ip + '&need3HourForcast=0&needAlarm=0&needHourData=0&needIndex=0&needMoreDay=0'
    info_json = api_request(ihost = host, ipath = path, iappcode = appcode, iquerys = querys)
    r = load_weather_json(info = info_json)

    return r

# 通过id获取天气情况
def get_weather_by_ip(iip):
    result = ''
    try:
        result = NewsWeather.objects.get(ip = iip)
        time_dif = string_toDatetime(get_now()) - result.date
        overdue = time_dif.total_seconds()/60/60
        # 超过5小时的记录更新一次
        if overdue > 500:
            print('do this............')
            result.weather_info = get_weather_info(ip = iip)
            result.date = get_now()
            result.save()
    except ObjectDoesNotExist:
        info = get_weather_info(ip = iip)
        result = NewsWeather.objects.create(ip = iip, weather_info = info, date = get_now())

    return result
