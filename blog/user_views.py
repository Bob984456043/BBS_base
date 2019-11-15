from  rest_framework import views
from  . import models
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.
class LoginAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        ret={}
        username=request.data.get('username')
        password = request.data.get('password')
        user_list = User.objects.filter(username=username,password=password)
        if not user_list:
            ret['msg']='用户名或密码错误'
        else:

            token,created = Token.objects.update_or_create(user=user_list[0])
            ret['id']=str(user_list[0].id)
            ret['username']=user_list[0].username
            ret['email']=user_list[0].email
            ret['token']=token.key
        return Response(ret)

class RegisterAPI(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        ret={}
        username=request.data.get('username')
        password = request.data.get('password')
        email=request.data.get('email')
        user_list = User.objects.filter(username=username)
        if user_list:
            ret['msg']='用户名已存在'
        else:
            user=User.objects.create(username=username,password=password,email=email)
            ret['id']=str(user.id)
            ret['username']=user.username
            ret['email']=user.email
        return Response(ret)
class UserDetailAPI(views.APIView):
    def get(self,request,*args,**kwargs):
        ret={}
        id=request.query_params.get('id')
        try:
            user = User.objects.get(id=id)
            ret['id']=str(user.id)
            ret['username']=user.username
            ret['email']=user.email
        except:
            ret['msg']='用户id不存在'
        return  Response(ret)

