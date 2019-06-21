from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kind/<str:cate_req>/', views.kind, name='kind'),
    path('detail/<str:key>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('keyword_search/', views.keyword_search, name='keyword-search'),
    path('test/', views.test),
]
