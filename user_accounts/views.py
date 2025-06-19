from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterProfileSerializer,CustomTokenObtainPairSerializer,ChangePasswordSerializer,ForgetPasswordSerializer,UserProfileSerializer
from .models import Profile
from .permission import IsUser
# Create your views here.
class RegisterProfileView(CreateAPIView):
    serializer_class = RegisterProfileSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProfileLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ForgetPasswordSerializer
    def patch(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'messages':'Succesfully logout'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error':'Invalid refresh token'},status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def patch(self, request):
        serilaizer = ChangePasswordSerializer(data=request.data,context={'request':request})
        if serilaizer.is_valid():
            serilaizer.save()
            return Response({'message':'Password Updated Succesdully'},status=status.HTTP_200_OK)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Changed the Password'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(RetrieveAPIView):
    permission_classes = [IsUser, IsAuthenticated]
    serializer_class = UserProfileSerializer
    def get_object(self):
        return self.request.user