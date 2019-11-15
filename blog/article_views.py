from  rest_framework import views
from  . import models
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.

class ArticleDetailAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        id = request.data.get('id')
        try:
            article = models.Article.objects.get(id=id)
            user=article.user
            ret['id']=article.id
            ret['title']=article.title
            ret['category']=article.category
            ret['content']=article.content
            ret['post_time']=article.post_time
            ret['views']=article.views
            ret['comments']=article.comments
            ret['user_id']=user.id
            ret['username']=user.username
            ret['email']=user.email

        except:
            ret['msg']='文章id不存在'
