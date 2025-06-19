from .models import Profile
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_password1

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
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['profile_type'] = user.profile_type
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password1])
    confirm_new_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password':'Old password is incorrect'})
        if attrs['password1'] == attrs['new_password']:
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
    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phonenumber = PhoneNumberField(region='IN')
    new_password = serializers.CharField(write_only=True, validators=[validate_password1])
    confirm_new_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        phonenumber = attrs.get('phonenumber')
        if not Profile.objects.filter(phonenumber=phonenumber).exists():
            raise ValidationError("phonenumber does not exists in the database")
        if not Profile.objects.filter(email=email).exists():
            raise ValidationError("Email does not exists in the database")
        if not Profile.objects.filter(email=email , phonenumber=phonenumber).exists():
            raise ValidationError("Email and the password does not match to the same user")
        if attrs['new_password'] != attrs['confirm_new_password']:
           raise ValidationError("Password doesnot match")
        return attrs
    def save(self, **kwargs):
        email = self.validated_data['email']
        phonenumber = self.validated_data['phonenumber']
        user = Profile.objects.get(email=email, phonenumber=phonenumber)
        new_password = self.validated_data.pop('new_password')
        user.set_password(new_password)
        user.save()
        return user