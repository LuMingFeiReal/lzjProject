from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .toolsPublic import verifycode
# Create your views here.

# 模板全局变量
def global_settings(request):
    return {
        'SUCCESS': settings.SUCCESS,
        'USER_EXISTS': settings.USER_EXISTS,
        'DIFFERENT_PASSWORD': settings.DIFFERENT_PASSWORD,
        'ERROR_VERIFY_CODE': settings.ERROR_VERIFY_CODE,
        'ERROR_PASSWORD': settings.ERROR_PASSWORD,
        'ILLEGAL_REQUEST': settings.ILLEGAL_REQUEST,
        'SERVER_ERROR': settings.SERVER_ERROR
    }


def get_verifycode(request):
    buf = verifycode(request = request)
    # print(request.session['verifycode'])
    return HttpResponse(buf.getvalue(), 'image/png')
