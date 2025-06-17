from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterProfileSerializer,CustomTokenObtainPairSerializer
# Create your views here.
class RegisterProfileView(CreateAPIView):
    serializer_class = RegisterProfileSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProfileLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'messages':'Succesfully logout'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error':'Invalid refresh token'},status=status.HTTP_400_BAD_REQUEST)
