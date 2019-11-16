from rest_framework import serializers
from . import models
class ArticleSerializer(serializers.ModelSerializer):
    id=serializers.CharField()
    views = serializers.CharField()
    comments = serializers.CharField()
    user_id = serializers.CharField()
    username=serializers.CharField
    # title=serializers.CharField()
    # category=serializers.CharField()
    # content=serializers.CharField()
    # post_time=serializers.DateField()
    # views=serializers.IntegerField()
    # comments=serializers.IntegerField
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        model=models.Article
        fields="__all__"