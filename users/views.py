from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


@api_view(["GET"])
def get_users(request):
    users = UserSerializer(User.objects.all(), many=True).data
    return Response(users, status=status.HTTP_200_OK)
