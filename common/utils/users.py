import re
from django.contrib.auth.backends import ModelBackend
from users.models import User
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

# 根据用户名或者手机号获取用户
def get_user_by_account(account):
    try:
        #　手机号登陆的用户
        if re.match(r"1[3-9]\d{9}",account):
            user = User.objects.get(mobile=account)
        else:
            # 使用账号登陆的用户
            user = User.objects.get(username=account)
    except Exception as e:
        user = None

    return user


# 自定义认证后端
class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户名和手机号认证"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据username 查询用户
        user = get_user_by_account(username)
        # 判断用户是否尊在和密码是否正确
        if user and user.check_password(password):
            return user

        return None