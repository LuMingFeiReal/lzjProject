from django.urls import path
from . import views

urlpatterns = [
    path('get_verifycode/', views.get_verifycode, name = 'get_verifycode'),
]
