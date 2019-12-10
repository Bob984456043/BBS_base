from django.urls import path
from . import file_views
urlpatterns = [

    path('file/detail',file_views.FileDetailAPI.as_view()),
    path('files',file_views.FileQureyAPI.as_view()),

]
