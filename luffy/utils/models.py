from django.db import models


# 以后其他表也可能会用
class BaseModel(models.Model):
    # 是否删除
    # 是否展示
    # 上传时间
    # 最后更新时间。。。
    # 优先级
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否上架')
    orders = models.IntegerField(verbose_name='优先级')

    # 这样写，一迁移数据，会生成一个BaseModel表在数据库中
    class Meta:
        abstract = True  # 如果写了它， 表示虚拟表，不在数据库中生成，只做继承用