from  rest_framework import views
from  . import models,blog_serializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 20

class CommentQueryAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        article_id=request.query_params.get('article_id')
        comment_list=models.Comment.objects.filter(article_id=article_id)
        paginate=CommentPagination()
        page_list=paginate.paginate_queryset(comment_list,request)
        comment_serializer=blog_serializer.CommentSerializer(page_list,many=True)

        ret['list']=comment_serializer.data
        ret['total']=len(comment_list)
        return Response(ret)

class CommentDetailAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        id = request.query_params.get('id')
        try:
            comment = models.Comment.objects.get(id=id)
            serializer = blog_serializer.CommentSerializer(comment)
            ret = serializer.data
            return Response(ret)
        except:
            ret['msg']='评论id不存在'
            return Response(ret)

    def post(self,request,*args,**kwargs):
        ret={}
        content=request.data.get('content')
        post_time=request.data.get('post_time')
        article_id=request.data.get('article_id')
        user_id=request.data.get('user_id')
        article=models.Comment.objects.create(content=content,post_time=post_time,user_id=user_id,article_id=article_id)
        comment_serializer=blog_serializer.CommentSerializer(article)
        return Response(comment_serializer.data)

    def delete(self,request,*args,**kwargs):
        ret={}
        id=request.query_params.get('id')
        try:
            models.Comment.objects.get(id=id).delete()
        except:
            ret['msg']='评论不存在'
        return Response(ret)




