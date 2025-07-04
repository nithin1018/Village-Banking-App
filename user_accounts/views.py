from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile,Account,Transaction
from .permission import IsUser,IsAdmin
from .services import handle_transaction
from .utils import get_account_balance
from .serializers import RegisterProfileSerializer,CustomTokenObtainPairSerializer,ChangePasswordSerializer,ForgetPasswordSerializer,UserProfileSerializer,AdminDashboardSerializer,TransactionInputSerializer,TransactionOutputSerializer,AccountDetailedModelSerializer,UserForAdminSerializer,TransactionListForAdminSerializer,TransactionModelSerializerForAdmin,SentOtpSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TransactionFilter,ProfileFilter
from rest_framework import filters
from .utils import send_otp_email
from .throttles import OTPThrottle
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
# Create your views here.
#For registering any type of users
class RegisterProfileView(CreateAPIView):
    serializer_class = RegisterProfileSerializer

#Used for obtaining the access token and the refresh toekn
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#used to logout any users
class ProfileLogoutView(APIView):
    throttle_classes = [UserRateThrottle]
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

#used to update the password of the logined user
class UpdatePasswordView(APIView):
    throttle_classes = [UserRateThrottle]
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def patch(self, request):
        serilaizer = ChangePasswordSerializer(data=request.data,context={'request':request})
        if serilaizer.is_valid():
            serilaizer.save()
            return Response({'message':'Password Updated Successully'},status=status.HTTP_200_OK)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)

#used to to get the otp for the user
class SendOtpView(APIView):
    throttle_classes = [OTPThrottle]
    def post(self, request):
        serializer = SentOtpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            send_otp_email(user,"Forgot Password")
            return Response({"message":"Otp sent successfully"},status=status.HTTP_200_OK)
        return Response({"error":"Otp send failed"},status=status.HTTP_400_BAD_REQUEST)

#used to change the password is password is forgotten can be used when not logged in 
class ForgotPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = ForgetPasswordSerializer
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Changed the Password'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#full details of the user profile,transaction,account
class UserProfileView(RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsUser, IsAuthenticated]
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['id','timestamp']
    ordering = ['id']
    def get_object(self):
        return self.request.user
    
#Detailed view of an account using the id will get the profile and account
class AccountProfileDetailedView(RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = AccountDetailedModelSerializer
    queryset = Account.objects.all()

#Detailed view of the admin will get the total users,balance and the admin details
class AdminDashboardView(APIView):
    throttle_classes = [UserRateThrottle]
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
    
#for getting the list of user for admin
class AdminDashboardUserView(ListAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdmin, IsAuthenticated]
    serializer_class = UserForAdminSerializer
    queryset = Profile.objects.filter(profile_type='user').order_by('created_at')
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ProfileFilter
    ordering_fields = ['first_name','age','created_at']
    ordering = ['created_at']

#for getting the detailed view of the user for admin
class AdminDashboardUserDetailedView(RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdmin, IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.filter(profile_type='user')
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id','timestamp']
    ordering = ['id']

#for getting the list of transaction for admin
class AdminDashboardTransactionView(ListAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdmin, IsAuthenticated]
    serializer_class = TransactionListForAdminSerializer
    queryset = Transaction.objects.all().order_by('timestamp')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['id','timestamp']
    ordering = ['id']

#for getting the detailed view of the transaction for admin
class AdminDashboardTransactionDetailedView(RetrieveAPIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdmin, IsAuthenticated]
    serializer_class = TransactionModelSerializerForAdmin
    queryset = Transaction.objects.all()

#Full Transaction logic of withdraw, transfer and deposit the amount to the account 
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
