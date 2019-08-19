from django.shortcuts import render

# Create your views here.

# 用户注册
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from users.serializer import RegisterUserCreateSerializer
from rest_framework_jwt.views import ObtainJSONWebToken


class TestView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        return Response({"ok"})


# users.py create
class RegisterUserCreateView(CreateAPIView):
    """
    post: /users.py/
    """
    # 加载序列化器
    serializer_class = RegisterUserCreateSerializer

# users.py login
class UserAuthorizationView(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        # 调用jwt扩展的方法
        response = super().post(request)

        # 如果登陆成功
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 用户登陆成功
            user = serializer.validated_data.get("user")

        return response


