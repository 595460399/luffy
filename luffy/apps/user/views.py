from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet

from django.conf import settings
from django.core.cache import cache

from libs.sms import gen_code
from libs.sms import send_sms_v3
from .models import User
from .serializer import LoginSerializer, MobileSerializer, RegisterSerializer
# Create your views here.
from utils.response import APIResponse


class LoginView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @action(methods=['POST'], detail=False, )  # user/login/mul_login
    def mul_login(self, request):
        return self._login(request)

    @action(methods=['POST'], detail=False, )  # user/login/mobile_login
    def mobile_login(self, request):
        return self._login(request)

    def get_serializer_class(self):
        # print(self.action)
        print(self.action)
        if self.action == 'mul_login':
            return self.serializer_class
        else:
            return MobileSerializer

    def _login(self, request):
        try:
            # 校验规则和签发token都写到序列化类中
            ser = self.get_serializer(data=request.data, context={'request': request})
            ser.is_valid(raise_exception=True)  # 走序列化类的字段自己的规则，局部钩子和全局钩子
            token = ser.context.get('token')
            username = ser.context.get('username')
            icon = ser.context.get('icon')
        except Exception as e:
            raise APIException(str(e))
        return APIResponse(token=token, username=username, icon=icon)


class UserView(ViewSet):
    # /user/user_info/check_mobile---->post请求
    @action(methods=['POST'], detail=False, )
    def check_mobile(self, request):
        mobile = request.data.get('mobile')
        # res=User.objects.filter(mobile=mobile).first()
        try:
            User.objects.get(mobile=mobile)  # 有且只有一个才行，否则报错
            # 一堆逻辑
        except Exception as e:
            # return APIResponse(is_exisit=False)# {code:100,msg:'成功',is_exisit=false}
            raise APIException('该手机号不存在')  # {code:888,msg:'手机号不存在'}

        return APIResponse(is_exisit=True)  # {code：100，msg：成功，is_exisit:true}

    @action(methods=['GET'], detail=False, )
    def send_sms(self, request):
        phone = request.query_params.get('phone')
        sms_code = gen_code()
        # res = send_sms_v2(phone, sms_code)
        cache.set(settings.SMS_CODE_CACHE % phone, sms_code)
        print(sms_code)
        if settings.DEBUG is False:
            res = send_sms_v3(phone, sms_code)
            if res:
                return APIResponse()
            else:
                return APIResponse(code=101, msg='发送失败，请稍后再试')
        else:
            return APIResponse()

    # @action(methods=['POST'], detail=False)
    # def upload_icon(self, request):
    #     icon = request.data.get('icon')


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        # ser=self.get_serializer(data=request.data)
        # ser.is_valid(raise_exception=True)
        # ser.save() # 如果是新增，会触发序列化类的create，如果是修改，会触发序列化类的update
        return APIResponse(msg='注册成功', user=res.data)  # {code:100,msg:注册成功，data:{mobile:122}}
