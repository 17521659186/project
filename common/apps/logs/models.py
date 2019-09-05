from django.db import models


# Create your models here.
from robots.models import RobotModel


class QaLogMOdel(models.Model):
    bot_id = models.CharField(max_length=64, verbose_name="机器人id")
    user_id = models.CharField(max_length=64, verbose_name="用户id")
    conversion_id = models.CharField(max_length=64, verbose_name="回话id")
    question = models.TextField(max_length=64, verbose_name="问题")
    answer = models.TextField(max_length=64, verbose_name="答案")
    intent = models.CharField(max_length=64, verbose_name="意图")
    create_time = models.DateTimeField(verbose_name="创建时间")


    class Meta:
        db_table = "t_qa_log"
        verbose_name = "会话日志"
        verbose_name_plural = verbose_name
