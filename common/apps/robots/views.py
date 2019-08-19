import os
import shutil
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.settings import TRAIN_DATA_PATH_PREFIX, TRAIN_URL,PUBLISH_URL
from robots.models import RobotModel
import requests

from robots.serializer import ShowRobotSerilizer
from users.models import User
# Create your views here.


# show　all robot
class ShowRobotViews(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # query robot
        try:
            user = User.objects.get(id=request.user.id)
        except Exception as e:
            user = None

        data = None
        try:
            if user:
                data = ShowRobotSerilizer(user.user_robot.all(),many=True).data
        except Exception as e:
            data = None

        return Response({"data":data},status=status.HTTP_200_OK)


# create a new robot
class CreateRobotViews(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # get request params
        bot_id = request.data.get("bot_id", None)
        version = request.data.get("version", None)

        # check params
        if not all([bot_id, version]):
            return Response({"message": "缺少bot_id or version"}, status=status.HTTP_400_BAD_REQUEST)
        # make dir
        # if os.path.exists(TRAIN_DATA_PATH_PREFIX + bot_id + "/" + version):
        #     return Response({"message": "不能重复创建"}, status=status.HTTP_400_BAD_REQUEST)
        # os.makedirs(TRAIN_DATA_PATH_PREFIX + bot_id + "/" + version)
        try:
            shutil.copytree(TRAIN_DATA_PATH_PREFIX+"common",TRAIN_DATA_PATH_PREFIX + bot_id + "/" + version)
        except Exception as e:
            return Response({"message": "不能重复创建"}, status=status.HTTP_400_BAD_REQUEST)

        # save model
        try:
            robot = RobotModel.objects.filter(bot_id=bot_id, mode="test", user_id=request.user.id).first()
            if robot:
                robot.version = version
            else:
                robot = RobotModel(bot_id=bot_id, version=version, mode="test", user_id=request.user.id,
                               update_time=datetime.now())
            robot.save()
        except Exception as e:
            # delete train path
            os.removedirs(TRAIN_DATA_PATH_PREFIX + bot_id + "/" + version)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)


# train robot
class TrainRobotView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # get request params
        bot_id = request.data.get("bot_id", None)
        version = request.data.get("version", None)

        # check params
        if not all([bot_id, version]):
            return Response({"message": "缺少bot_id or version"}, status=status.HTTP_400_BAD_REQUEST)

        r = requests.post(url=TRAIN_URL,
                          json={"bot_id":bot_id,"version":version})

        if r.status_code != 200:
            return Response({"message": "train failed "}, status=status.HTTP_400_BAD_REQUEST)

        # update model


        return Response({"message":"train ok"},status=status.HTTP_200_OK)


# publish robot
class PublishRobot(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        # get request params
        bot_id = request.data.get("bot_id", None)
        version = request.data.get("version", None)

        # check params
        if not all([bot_id, version]):
            return Response({"message": "缺少bot_id or version"}, status=status.HTTP_400_BAD_REQUEST)

        r = requests.post(url=PUBLISH_URL,
                          json={"bot_id": bot_id, "version": version})


        if r.status_code != 200:
            return Response({"message": "publish failed "}, status=status.HTTP_400_BAD_REQUEST)

        try:
            robot = RobotModel.objects.filter(bot_id=bot_id,version=version,mode="product").first()
            robot.user_id = request.user.id
            robot.save()
        except Exception as e:
            return Response({"message": "publish failed "}, status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.get(id=1)


        return Response({"message": "publish ok"}, status=status.HTTP_200_OK)



