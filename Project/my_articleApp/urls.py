from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall, name='wall'),
    path('addpage/', views.add_page, name='addpage'),
    path('addArticle/', views.add_article, name='add_article'),
    # path('getArticles', views.get_all_articles, name='get_articles'),
    path('removeArticle/', views.remove_article, name='remove_article'),
]
