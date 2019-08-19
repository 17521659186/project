from django.conf.urls import url
from . import views

urlpatterns = [
    # user create
    url(r"^register$", views.RegisterUserCreateView.as_view()),

    # user login
    url(r"^login$",views.UserAuthorizationView.as_view()),

    url("^test$",views.TestView.as_view())




]