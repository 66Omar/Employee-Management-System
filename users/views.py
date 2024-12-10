from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
