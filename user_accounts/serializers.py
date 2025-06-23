from .models import Profile,Account,Transaction
from rest_framework import serializers,status
from rest_framework.exceptions import ErrorDetail
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.response import Response
from django.utils import timezone
from .validators import validate_password1,validate_name,validate_amount
from datetime import timedelta
from django.contrib.auth.hashers import check_password
#For creating a user registration form
class RegisterProfileSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password1])
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = Profile
        fields = ['first_name','last_name','age','email','phonenumber','password1','password2','profile_type','employee_id','profile_pic']
    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value
    def validate_phonenumber(self, value):
        if Profile.objects.filter(phonenumber=value).exists():
            raise ValidationError('PhoneNumber already exists!!!')
        return value
    def validate(self, attrs):
        profile_type = attrs.get('profile_type')
        employee_id = attrs.get('employee_id')
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('Password doesnot match!!!!')
        if profile_type in ['admin', 'staff'] and not employee_id:
            raise ValidationError("Employee id is required")
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        profile_type = validated_data.get('profile_type')
        user = Profile(**validated_data)
        if profile_type == 'staff':
            user.is_staff = True
        if profile_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
        user.set_password(password)
        user.save()
        return user
    
#for the custom logic of the value of the token 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['profile_type'] = user.profile_type
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
    
#serializer for changing the password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password1])
    confirm_new_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password':'Old password is incorrect'})
        if attrs['old_password'] == attrs['new_password']:
            raise ValidationError("Old password and new password cannot be same")
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise ValidationError("Password doesnot match")
        return attrs
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
    
#class for sending otp to the email
class SentOtpSerializer(serializers.Serializer):
    email =  serializers.CharField()
    def validate(self, attrs):
        email = attrs['email']
        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise ValidationError({
                "User doesn't exist":ErrorDetail("User with thei provided email doesnt exist",code="invalid_email")
            })
        attrs['user'] = user
        return attrs
#serializer for the forgot password    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password1])
    confirm_new_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise ValidationError({
                "Profile":ErrorDetail("Email doesnt exist in the database",code="Invalid_email")
            })
        if not user.otp:
            raise ValidationError({
                "otp": ErrorDetail("No OTP was requested or it has expired.", code="no_otp")
    })
        if not check_password(otp, user.otp):
            raise ValidationError({
                "otp":ErrorDetail("Invalid Otp",code="invalid_otp")
            })
        now = timezone.now()
        expiry_time = user.otp_created_time + timedelta(minutes=1)
        if now > expiry_time:
            raise ValidationError({
            "otp":ErrorDetail("Otp expired please request for another otp",code="otp_expired")
        })
        if attrs['new_password'] != attrs['confirm_new_password']:
           raise ValidationError("Password doesnot match")
        return attrs
    
    def save(self, **kwargs):
        email = self.validated_data['email']
        user = Profile.objects.get(email=email)
        new_password = self.validated_data.pop('new_password')
        user.set_password(new_password)
        user.save()
        return user

#used for getting the full details of a particular user that is profile,account and the transaction for the view UserProfileView
class TransactionModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = ['transaction_type','sender','receiver','amount','status','description','timestamp']
class AccountModelSerializer(serializers.ModelSerializer):
        sender = TransactionModelSerializer(source='sender_transaction',many=True, read_only=True)
        receiver = TransactionModelSerializer(source='receiver_transaction',many=True, read_only=True)
        class Meta:
            model = Account
            fields = ['account_number','balance','created_at','sender','receiver']
class UserProfileSerializer(serializers.ModelSerializer):
    account = AccountModelSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['first_name','last_name','age','phonenumber','profile_pic','account']

#used for getting the full details of a particular user that is profile,account and the transaction for the view UserProfileView
class UserProfileSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','age','phonenumber','profile_pic']
class AccountModelSerializerForAdmin(serializers.ModelSerializer):
        user = UserProfileSerializerForAdmin(read_only=True)
        class Meta:
            model = Account
            fields = ['user','account_number','balance','created_at']
class TransactionModelSerializerForAdmin(serializers.ModelSerializer):
        sender = AccountModelSerializerForAdmin(read_only=True)
        receiver = AccountModelSerializerForAdmin(read_only=True)
        class Meta:
            model = Transaction
            fields = ['transaction_type','sender','receiver','amount','status','description','timestamp']



#for getting the profile account and the profile for getting the details user by user in the AccountProfileDetailedView
class UserProfileDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','age','phonenumber','profile_pic','account']
class AccountDetailedModelSerializer(serializers.ModelSerializer):
    user = UserProfileDetailedSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['account_number','balance','created_at','user']

#For the AdminDashboard
class AdminDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['password']

#for getting the user's list for admin
class UserForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','email','phonenumber']

#for getting thee transaction list for admin
class TransactionListForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount','transaction_type','sender','receiver','status']

#for the transaction view for accpeting the details for the transaction and also the ouput as timestamp and the status of the payment
class TransactionInputSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=6, required=True)
    transaction_type = serializers.ChoiceField(required=True, choices=Transaction.TRANSACTION_TYPE)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True, validators=[validate_amount])
    description = serializers.CharField(default="",allow_blank=True)
    receiver_account_number = serializers.CharField(default="",allow_blank=True)
    def validate(self, attrs):
        receiver_account_number = attrs.get('receiver_account_number')
        transaction_type = attrs.get('transaction_type')
        request=self.context['request']
        receiver = None
        if receiver_account_number:
            try:
                receiver = Account.objects.get(account_number=receiver_account_number)
            except Account.DoesNotExist:
                raise ValidationError({
                    "reciever_account_number":ErrorDetail("Reciever Account number doesnt exist.",code="invalid_account_number")
                })
        try:
            user = Profile.objects.get(email=request.user.email)
            acc = user.account.account_number
        except Profile.DoesNotExist:
            return Response({'detail':'profile not found'},status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({'detail':'account not found'},status=status.HTTP_400_BAD_REQUEST)
        if acc == receiver:
            raise ValidationError({
               "reciever_account_number":ErrorDetail("You cant self transfer",code="transfer mismatch")
            })
        if transaction_type == 'transfer' and not receiver_account_number:
            raise ValidationError({
                "reciever_account_number":ErrorDetail("Reciever account type when the transaction type is transfer",code='invalid_reciever_account')
            })
        return attrs
class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['status','timestamp']

