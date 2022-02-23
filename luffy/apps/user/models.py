from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)  # 唯一
    # 需要pillow包的支持
    icon = models.ImageField(upload_to='icon', default='icon/default.png')

    class Meta:
        db_table = 'luffy_user'  # 如果不配它，表名是  app名字_类名小写
        verbose_name = '用户表'  # 在admin中显示的表名
        verbose_name_plural = verbose_name  # 在admin中显示的表名,不配它会加个s

    def __str__(self):  # print(对象) 的时候，触发它的执行
        return self.username
