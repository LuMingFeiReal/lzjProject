from django.urls import path
from . import views

urlpatterns = [
    path('personal/', views.personal, name = 'personal'),
    path('update_info/', views.update_info, name = 'update_user'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('get_history/', views.get_history, name = 'get_history'),
    path('get_articles/', views.get_all_articles, name = 'get_articles'),
    path('get_interest/', views.get_interest, name='get_interest'),
    path('get_check/', views.get_article_check, name='get_check'),
    path('pass_check/', views.pass_check, name='pass_check')
]
