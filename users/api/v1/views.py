from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# trail changes for git