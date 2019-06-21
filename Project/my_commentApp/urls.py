from django.urls import path
from . import views

urlpatterns = [
    # path('get_comment/<str:key>/', views.get_comment, name = 'get_comment'),
    path('add_comment/', views.add_comment, name = 'add_comment'),
]
