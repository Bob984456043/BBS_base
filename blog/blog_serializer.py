from rest_framework import serializers
from . import models
class ArticleSerializer(serializers.Serializer):
    # id=serializers.IntegerField()
    # title=serializers.CharField()
    # category=serializers.CharField()
    # content=serializers.CharField()
    # post_time=serializers.DateField()
    # views=serializers.IntegerField()
    # comments=serializers.IntegerField
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        model=models.Article
        fields='__all__'