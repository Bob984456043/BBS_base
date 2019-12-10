
from django.db import models
from django.contrib.auth.models import User


# def upload_to(instance, fielname):
#     return '/'.join([BASE_DIR, instance.user_name, filename])

class File(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    post_time = models.DateTimeField()
    downloads = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=100,default='static/file')  # 文件储存路径
    filesize = models.IntegerField()
    filebrief = models.CharField(max_length=100,default='brief')

    class Meta():
        db_table = "filesys"
