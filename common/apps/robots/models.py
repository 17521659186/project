from django.db import models


# Create your models here.
from users.models import User


class RobotModel(models.Model):
    bot_id = models.CharField(max_length=64, verbose_name="机器人id")
    version = models.CharField(max_length=64, verbose_name="机器人版本号")
    mode = models.CharField(max_length=64, verbose_name="机器人版本号")
    update_time = models.DateTimeField(verbose_name="机器人版本号")
    user = models.ForeignKey(User, related_name='user_robot', null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='用户')

    class Meta:
        db_table = "t_publish_setting"
        verbose_name = "机器人"
        verbose_name_plural = verbose_name


