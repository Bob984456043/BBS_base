
from django.urls import path
from . import user_views,article_views
urlpatterns = [
    path('user/login', user_views.LoginAPI.as_view()),
    path('user/register', user_views.RegisterAPI.as_view()),
    path('user/detail', user_views.UserDetailAPI.as_view()),

    path('article/detail',article_views.ArticleDetailAPI.as_view())
]
