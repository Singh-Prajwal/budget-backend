# backend/users/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer
from .models import CustomUser

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """Custom login view that uses our custom serializer."""
    serializer_class = MyTokenObtainPairSerializer