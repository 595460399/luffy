from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Banner)
class EmployeAdmin(admin.ModelAdmin):
    # 一行数据显示哪些字段
    list_display = ('id', 'title', 'link', 'is_show')

    # 增加自定义按钮
    actions = ['make_copy']

    def make_copy(self, request, queryset):
        # 点击触发它
        # queryset：选中的数据
        # request 请求对象
        print(queryset)

    make_copy.short_description = '我叫按钮'
    make_copy.confirm = '你是否执意要点击这个按钮？'
