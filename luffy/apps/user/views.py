from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.viewsets import GenericViewSet, ViewSet
from .models import User
from .serializers import LoginSerializer
# Create your views here.
from utils.response import APIResponse


class LoginView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @action(methods=['POST'], detail=False, )  # user/login/mul_login
    def mul_login(self, request):
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

    # /user/check_mobile---->post请求
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
