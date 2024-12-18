from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_users),
    path("auth/register", views.RegisterView.as_view(), name="register"),
    path("auth/login", views.LoginView.as_view(), name="login"),
]
