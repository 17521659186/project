from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from logs.models import QaLogMOdel
from logs.serializer import ShowQaLogSerilizer


# Create your views here.


# robot qa log
class RobotQaLogView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bot_id = request.data.get("bot_id", None)

        if not bot_id:
            return Response({"messge": "缺少参数"}, status=status.HTTP_400_BAD_REQUEST)

        # query qa log
        try:
            logs = QaLogMOdel.objects.filter(bot_id=bot_id, user_id=request.user.id).all()
        except Exception as e:
            logs = None

        # get serilizer data
        data = None
        try:
            if logs:
                data = ShowQaLogSerilizer(logs, many=True).data
        except Exception as e:
            data = None

        return Response({"data": data}, status=status.HTTP_200_OK)
