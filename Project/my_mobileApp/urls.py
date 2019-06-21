from django.urls import path
from . import views

urlpatterns = [
    path('', views.mhome, name = 'mhome'),
    path('gethomeinfo', views.get_home_news, name = 'getnews'),
    path('kind/<str:cate_req>/', views.mkind, name = 'mkind'),
    path('getkindinfo/', views.get_kind_news, name = 'getkindnews'),
    path('detail/<str:unkey>/', views.mdetail, name = 'mdetail')
]
