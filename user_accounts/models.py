from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_name,validate_age
# Create your models here.
class Profile(AbstractUser):
    PROFILE_CHOICES = [
        ('user','User'),
        ('staff','Staff'),
        ('admin','Admin'),

    ]
    first_name = models.CharField(max_length=100,blank=False,null=False,validators=[validate_name])
    last_name = models.CharField(max_length=100,blank=False,null=False,validators=[validate_name])
    age = models.IntegerField(blank=True,null=True,validators=[validate_age])
    email = models.EmailField(unique=True, blank=False,null=False)
    phonenumber = PhoneNumberField(unique=True,region='IN')
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES,default='user')
    account_number = models.CharField(max_length=20,blank=True,null=True)
    employee_id = models.CharField(max_length=20,blank=True,null=True)
    profile_pic = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'