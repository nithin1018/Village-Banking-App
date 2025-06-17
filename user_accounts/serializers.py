from .models import Profile
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .validators import validate_password1

class RegisterProfileSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password1])
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = Profile
        fields = ['first_name','last_name','age','email','phonenumber','password1','password2','profile_type','account_number','employee_id','profile_pic']

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
        account_number = attrs.get('account_number')
        employee_id = attrs.get('employee_id')
        if attrs['password1'] != attrs['password2']:
            raise ValidationError('Password doesnot match!!!!')
        if profile_type == 'user' and not account_number:
            raise ValidationError("Account Number is required")
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