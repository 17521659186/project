from django.conf.urls import url
from . import views

urlpatterns = [
    # qalog show
    url(r"^show$", views.RobotQaLogView.as_view()),

]