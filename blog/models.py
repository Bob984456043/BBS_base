from django.db import models
from django.contrib.auth.models import User



class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    content=models.TextField()
    post_time=models.DateTimeField()
    views=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table='article'

class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    content=models.CharField(max_length=1000)
    post_time=models.DateTimeField()
    stars=models.IntegerField(default=0)
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    username=models.CharField(max_length=50,default='')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table='comment'
# class Comment_reply(models.Model):
#     id=models.AutoField(primary_key=True)
#     comment_id=models.IntegerField()
#     reply_id=models.IntegerField()
#     reply_type=models.CharField(max_length=50)
#     content=models.CharField(max_length=1000)
#     from_id=models.IntegerField()
#     to_id=models.IntegerField()