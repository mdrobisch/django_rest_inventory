from rest_framework import generics, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User

class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
