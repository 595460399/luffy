from rest_framework import serializers
from .models import User
import re
from rest_framework.exceptions import ValidationError

# from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from rest_framework_jwt.views import obtain_jwt_token


class LoginSerializer(serializers.ModelSerializer):
    # 如果不重写username，username字段自己的校验规则就过不了
    # 如果不重写，字段自己的校验规则（从User表身上映射过来的），最长和最短，由于username是 unique的
    username = serializers.CharField()  # 字段自己的校验规则就没了

    class Meta:
        model = User
        # 往里走--->反序列化校验：username和password---》只是校验长短
        # 往外走--->序列化---》username，icon
        fields = ['username', 'password', 'icon']
        extra_kwargs = {
            'password': {'write_only': True},
            'icon': {'read_only': True}
        }

    def validate(self, attrs):  # 全局钩子
        # 校验用户名和密码是否正确，如果正确，签发token，如果不正确，抛异常
        # 1 获取登录用户
        user = self._get_user(attrs)
        # 2 签发token--django-jwt

        token = self._get_token(user)

        # 3 把token 放入到当前对象中给view用
        self.context['token'] = token
        self.context['username'] = user.username
        # self.context['icon']=user.icon # icon的有点问题
        # 这个地址是服务端地址，服务端地址从request对象中可以取出request.META['HTTP_HOST']
        request = self.context.get('request')
        self.context['icon'] = 'http://%s/media/' % request.META['HTTP_HOST'] + str(user.icon)
        return attrs

    def _get_user(self, attrs):  # 公司里这么写，表示只在类内部用
        # 取出用户的用户名和密码，校验
        username = attrs.get('username')  # 可能是手机号，邮箱和用户名
        password = attrs.get('password')
        # 正则匹配
        if re.match(r'^1[3-9][0-9]{9}$', username):  # 手机号
            user = User.objects.filter(mobile=username).first()
        elif re.match(r'^.+@.+$', username):  # 邮箱
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            # 校验密码
            return user
        else:
            raise ValidationError('用户名或密码错误')

    def _get_token(self, user):
        # 根据user获取payload
        payload = jwt_payload_handler(user)
        # 根据payload得到token
        token = jwt_encode_handler(payload);
        return token
