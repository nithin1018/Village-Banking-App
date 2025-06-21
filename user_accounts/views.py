from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterProfileSerializer,CustomTokenObtainPairSerializer,ChangePasswordSerializer,ForgetPasswordSerializer,UserProfileSerializer,AdminDashboardSerializer,TransactionInputSerializer,TransactionOutputSerializer,TransactionModelSerializer,AccountDetailedModelSerializer
from .models import Profile,Account
from .permission import IsUser,IsAdmin
from .services import handle_transaction
from .utils import get_account_balance
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
            return Response({'message':'Password Updated Successully'},status=status.HTTP_200_OK)
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
    
class AccountProfileDetailedView(RetrieveAPIView):
    permission_classes = [IsUser, IsAuthenticated]
    serializer_class = AccountDetailedModelSerializer
    queryset = Account.objects.all()

    
class AdminDashboardView(APIView):
    serializer_class = AdminDashboardSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    def get(self, request):
        current_user_data = AdminDashboardSerializer(request.user).data
        user_profiles = Profile.objects.filter(profile_type='users')
        no_of_user = user_profiles.count()
        bank_balance = get_account_balance()
        return Response(
            {'current_user':current_user_data,
            'no_of_user':no_of_user,
            'bank_balance':bank_balance
            },
            status=status.HTTP_200_OK
        )
class TransactionView(APIView):
    permission_classes = [IsUser]
    serializer_class = TransactionInputSerializer
    def post(self, request):
        serializer = TransactionInputSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            receiver_account_number = serializer.validated_data['receiver_account_number'] or None
            description = serializer.validated_data['description']
            transaction_type = serializer.validated_data['transaction_type']
            amount = serializer.validated_data['amount']
            receiver = None
            if receiver_account_number:
                receiver = Account.objects.get(account_number=receiver_account_number)
            try:
                txn = handle_transaction(
                    user_account=request.user.account,
                    receiver_account=receiver,
                    tran_type=transaction_type,
                    amt=amount,
                    desc=description,
                )
                print(type(txn))
                output = TransactionOutputSerializer(txn)
                return Response(output.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
