from  rest_framework import views
from  . import models
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
from . import blog_serializer
# Create your views here.
class LoginAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        ret={}
        user_serializer=blog_serializer.UserSerisalizer(data=request.data)
        if user_serializer.is_valid():
            user_list = User.objects.filter(username=user_serializer.validated_data.get('username'),
                                            password=user_serializer.validated_data.get('password'))
            if not user_list:
                ret['msg']='用户名或密码错误'
            else:
                token,created = Token.objects.update_or_create(user=user_list[0])
                ret=blog_serializer.UserSerisalizer(user_list[0]).data
                ret['token']=token.key
            return Response(ret)
        else:
            return Response(user_serializer.errors)

class RegisterAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        ret={}
        user_serializer = blog_serializer.UserSerisalizer(data=request.data)
        if user_serializer.is_valid():
            user_list = User.objects.filter(username=user_serializer.validated_data.get('username'))
            if user_list:
                ret['msg']='用户名已存在'
            else:
                user=user_serializer.create(user_serializer.validated_data)
                user_serializer=blog_serializer.UserSerisalizer(user)
                ret=user_serializer.data
            return Response(ret)
        else:
            return Response(user_serializer.errors)

class UserDetailAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        id=request.query_params.get('id')
        try:
            user = User.objects.get(id=id)
            user_serializer=blog_serializer.UserSerisalizer(user)
            ret=user_serializer.data
        except:
            ret['msg']='用户id不存在'
        return Response(ret)

