from django.shortcuts import redirect
from django.contrib import auth
from django.http import HttpResponse
from django.conf import settings
from .models import NewsUser
from my_toolsApp.toolsPublic import confirm_code


# Create your views here.
def login(request):
    name = request.POST.get("username")  # 获取用户名
    pwd = request.POST.get("password")  # 获取用户的密码
    code = request.POST.get('verifycode')

    msg = ''
    if confirm_code(request, code):
        user = auth.authenticate(username = name,password = pwd) # 验证用户名和密码，返回用户对象
        if user:      # 如果用户对象存在
            auth.login(request, user)
            msg = settings.SUCCESS
        else:
            msg = settings.ERROR_PASSWORD
    else:
        msg = settings.ERROR_VERIFY_CODE

    return HttpResponse(msg)


def logout(request):
    auth.logout(request)
    return redirect('home')


def register(request):
    name = request.POST.get('username')
    mail = request.POST.get('email')
    pwd = request.POST.get('password')
    repwd = request.POST.get('repassword')
    code = request.POST.get('verifycode')

    msg = ''
    if confirm_code(request, code):
        if pwd == repwd:
            if auth.models.User.objects.filter(username = name):
                msg = settings.USER_EXISTS
            else:
                user = auth.models.User.objects.create_user\
                    (username = name, password = pwd, email = mail)
                auth.login(request, user)
                msg = settings.SUCCESS
        else:
            msg = settings.DIFFERENT_PASSWORD
    else:
        msg = settings.ERROR_VERIFY_CODE
    # NewsUser.objects.
    return HttpResponse(msg)





# 增加用户
def test(request):
    user = auth.models.User.objects.create_user\
                    (username = 'aaa', password = 'aaa', email = 'aaa@mail')
    NewsUser.objects.create(uid = user, nickname = user.username, age = 0, sex = 1)


    user = auth.models.User.objects.create_user\
                    (username = 'bbb', password = 'bbb', email = 'bbb@mail')
    NewsUser.objects.create(uid = user, nickname = user.username, age = 0, sex = 1)

    user = auth.models.User.objects.create_user\
                    (username = 'ccc', password = 'ccc', email = 'ccc@mail')
    NewsUser.objects.create(uid = user, nickname = user.username, age = 0, sex = 1)

    user = auth.models.User.objects.create_user\
                    (username = 'ddd', password = 'ddd', email = 'ddd@mail')
    NewsUser.objects.create(uid = user, nickname = user.username, age = 0, sex = 1)
    return HttpResponse('successs')
