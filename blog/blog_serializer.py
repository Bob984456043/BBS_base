from rest_framework import serializers
from . import models
class ArticleSerializer(serializers.ModelSerializer):
    id=serializers.CharField(required=False)
    title=serializers.CharField(required=False)
    category=serializers.CharField(required=False)
    content=serializers.CharField(required=False)
    post_time=serializers.DateTimeField(required=False)
    views = serializers.CharField(required=False)
    comments = serializers.CharField(required=False)
    user_id=serializers.CharField(required=False)
    class Meta:
        model=models.Article
        fields=['id','title','category','content','post_time','views','comments','user_id']
class CommentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(required=False)
    content=serializers.CharField(required=False)
    post_time=serializers.DateTimeField(required=False)
    stars=serializers.CharField(required=False)
    article_id=serializers.CharField(required=False)
    user_id=serializers.CharField(required=False)
    username=serializers.CharField(required=False)
    class Meta:
        model=models.Comment
        fields=['id','content','post_time','stars','article_id','user_id','username']
class UserSerisalizer(serializers.ModelSerializer):
    id=serializers.CharField(required=False)
    username=serializers.CharField(required=False)
    password=serializers.CharField(write_only=True,required=False)
    email=serializers.EmailField(required=False)
    class Meta:
        model=models.User
        fields=['id','username','password','email']