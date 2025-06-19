from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_name,validate_age
from django.contrib.auth.models import BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class Profile(AbstractUser):
    username = None
    PROFILE_CHOICES = [
        ('user','User'),
        ('staff','Staff'),
        ('admin','Admin'),

    ]
    first_name = models.CharField(max_length=100,blank=False,null=False,validators=[validate_name])
    last_name = models.CharField(max_length=100,blank=False,null=False,validators=[validate_name])
    age = models.IntegerField(blank=False,null=False,validators=[validate_age])
    email = models.EmailField(unique=True, blank=False,null=False)
    phonenumber = PhoneNumberField(unique=True,region='IN')
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES,default='user')
    employee_id = models.CharField(max_length=20,blank=True,null=True)
    profile_pic = CloudinaryField('image',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class Account(models.Model):
    user = models.OneToOneField('Profile',on_delete=models.CASCADE,related_name='account')
    account_number = models.CharField(max_length=20,blank=True,null=True)
    balance = models.DecimalField(default=0.00,decimal_places=2,max_digits=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)