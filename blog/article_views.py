from  rest_framework import views
from  . import models,blog_serializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.

class ArticleDetailAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request,*args,**kwargs):
        ret={}
        id = request.query_params.get('id')
        try:
            article = models.Article.objects.get(id=id)
            # user=article.user
            # ret['id']=article.id
            # ret['title']=article.title
            # ret['category']=article.category
            # ret['content']=article.content
            # ret['post_time']=article.post_time
            # ret['views']=article.views
            # ret['comments']=article.comments
            # ret['user_id']=user.id
            # ret['username']=user.username
            # ret['email']=user.email
        except:
            ret['msg']='文章id不存在'
        serializer=blog_serializer.ArticleSerializer(article)
        ret=serializer.data
        return Response(ret)
    def post(self,request,*args,**kwargs):
        title=request.data.get('title')
        category=request.data.get('category')
        content=request.data.get('content')
        post_time=request.data.get('post_time')
        user_id=request.data.get('user_id')
        models.Article.objects.create(title=title,category=category,content=content,post_time=post_time,user_id=user_id)
        return Response({
            'title':title,
            'category':category,
            'content':content,
            'post_time':post_time,
            'user_id':user_id
        })