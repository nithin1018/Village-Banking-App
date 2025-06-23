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
    otp = models.CharField(max_length=128, blank=True, null=True)
    otp_created_time = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    def __str__(self):
        return f"{self.id} - {self.email}"

class Account(models.Model):
    user = models.OneToOneField('Profile',on_delete=models.CASCADE,related_name='account')
    account_number = models.CharField(max_length=20,blank=True,null=True,unique=True)
    balance = models.DecimalField(default=0.00,decimal_places=2,max_digits=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.account_number} -- {self.user.email}" 

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('withdraw','Withdraw'),
        ('deposit','Deposit'),
        ('transfer','Transfer'),
    ]
    STATUS_CHOICE = [
        ('success','Success'),
        ('failed','Failed'),
        ('pending','Pending'),
    ]
    transaction_type = models.CharField(max_length=12,choices=TRANSACTION_TYPE)
    sender = models.ForeignKey('Account',on_delete=models.SET_NULL,null=True,related_name='sender_transaction')
    receiver = models.ForeignKey('Account',on_delete=models.SET_NULL,null=True,related_name='receiver_transaction')
    amount = models.DecimalField(decimal_places=2,max_digits=12,blank=False,null=False)
    status = models.CharField(max_length=12,choices=STATUS_CHOICE,default='pending')
    description = models.TextField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)