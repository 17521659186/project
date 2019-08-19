import re

from rest_framework import serializers

from .models import User


class RegisterUserCreateSerializer(serializers.ModelSerializer):
    # 前端的数据　"username","mobile", "password""password2"
    # 手动添加字段
    password2 = serializers.CharField(label="确认密码",write_only=True,allow_null=False,allow_blank=False)
    # 增加token字段
    token = serializers.CharField(label="登陆状态token",read_only=True)

    class Meta:
        model = User
        # 验证字段
        fields = ["id", "username", "mobile", "password", "password2", "token"]

        # 额外参数和选项
        extra_kwargs = {

            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 验证手机号格式
    def validate_mobile(self, value):

        if not re.match(r"1[3-9]\d{9}", value):
            raise serializers.ValidationError("手机号格式正确")
        return value



    # 验证密码

    def validate(self, attrs):

        # 获取密码和短信验证码
        password = attrs.get("password")
        password2 = attrs.get("password2")


        # 判断密码是否一致
        if password != password2:
            raise serializers.ValidationError("密码不一致")

        return attrs

    # 创建模型
    def create(self, validated_data):
        # 删除反序列化不需要的字段
        del validated_data["password2"]

        # 反序列化操作
        # User.objects.create(**validated_data)

        user = super().create(validated_data)
        # 密码加密
        user.set_password(validated_data["password"])
        user.save()

        # 补充生成记录状态的token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 调用方法，把用户信息传给payload
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # token 信息给payload
        user.token = token

        return user



