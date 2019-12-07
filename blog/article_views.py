from  rest_framework import views
from  . import models,blog_serializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework.pagination import PageNumberPagination

class SelfPaginations(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 20

class ArticleQureyAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        user_id=request.query_params.get('id')
        category=request.query_params.get('category')
        if user_id!=None and category==None:
            article_list=models.Article.objects.filter(user_id=user_id)
        elif user_id!=None and category!=None:
            article_list=models.Article.objects.filter(user_id=user_id,category=category)
        elif user_id==None and category!=None:
            article_list = models.Article.objects.filter(category=category)
        elif user_id==None and category==None:
            article_list = models.Article.objects.all()

        paginate=SelfPaginations()
        page_list=paginate.paginate_queryset(article_list,request)
        article_serializer=blog_serializer.ArticleSerializer(page_list,many=True)

        ret['list']=article_serializer.data
        ret['total']=len(article_list)
        return Response(ret)

class ArticleDetailAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request,*args,**kwargs):
        ret={}
        id = request.query_params.get('id')
        try:
            print(id)
            article = models.Article.objects.get(id=id)
            serializer = blog_serializer.ArticleSerializer(article)
            ret = serializer.data
            return Response(ret)
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
        return Response(ret)
    def post(self,request,*args,**kwargs):
        title=request.data.get('title')
        category=request.data.get('category')
        content=request.data.get('content')
        post_time=request.data.get('post_time')
        user_id=request.data.get('user_id')
        article=models.Article.objects.create(title=title,category=category,content=content,post_time=post_time,user_id=user_id)
        return Response(blog_serializer.ArticleSerializer(article).data)

    def delete(self,request,*args,**kwargs):
        ret={}
        id=request.query_params.get('id')
        try:
            models.Article.objects.get(id=id).delete()
        except:
            ret['msg']='文章不存在'
        return Response(ret)

    def put(self,request,*args,**kwargs):
        ret={}
        id=request.data.get('id')
        article=models.Article.objects.get(id=id)
        old_article={
            'id':article.id,
            'title':article.title,
            'category':article.category,
            'content':article.content,
            'post_time':article.post_time,
            'views':article.views,
            'comments':article.comments,
            'user_id':article.user_id
        }
        for k,v in request.data.items():
            old_article[k]=v
        article_serializer=blog_serializer.ArticleSerializer(data=old_article)
        article_serializer.is_valid()
        article_serializer.update(article,validated_data=article_serializer.validated_data)
        return Response(old_article)
        # except:
        #     ret['msg']='文章不存在'
        #     return Response(ret)

