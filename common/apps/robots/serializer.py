from rest_framework import serializers
from robots.models import RobotModel


class ShowRobotSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RobotModel
        fields = ['id', 'bot_id', 'version', 'mode', 'update_time',"user"]