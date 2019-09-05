from rest_framework import serializers

from logs.models import QaLogMOdel


class ShowQaLogSerilizer(serializers.ModelSerializer):
    class Meta:
        model = QaLogMOdel
        fields = ['bot_id', 'question', 'answer', 'intent', 'create_time']




