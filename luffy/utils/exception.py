# 写一个函数
from rest_framework.views import exception_handler
from rest_framework.views import Response
from utils.logging import logger


def common_exception_handler(exc, context):
    # 只要进入到这个函数，就是出了异常，只要出了异常，就要记录日志
    # 日志要记录的尽量详细
    # exc：错误对象
    # context：中有请求对象，request对象，请求路径就在里面

    res = exception_handler(exc, context)

    # 也可以记录当前登录用户 context['request'].user
    path = context['request'].get_full_path()
    view_name = str(context['view'])
    logger.error('系统错误：请求地址是：%s，请求的试图类是：%s,错误原因是：%s' % (path, view_name, str(exc)))
    if res:  # 走了drf的异常
        return Response({'code': 888, 'msg': res.data['detail']})
    else:
        return Response({'code': 999, 'msg': '服务器异常，请联系系统管理员'})
