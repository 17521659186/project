from django.conf.urls import url
from . import views

urlpatterns = [
    # robot show
    url(r"^show", views.ShowRobotViews.as_view()),
    # robot create
    url(r"^create$", views.CreateRobotViews.as_view()),
    # robot train
    url(r"^train$", views.TrainRobotView.as_view()),
    # robot publish
    url(r"^publish$", views.PublishRobot.as_view()),
]