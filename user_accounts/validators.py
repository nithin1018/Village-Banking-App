from rest_framework.validators import ValidationError
import re

def validate_password1(password):
    if len(password) < 6:
        raise ValidationError("Password must have atleast 6 characters")
    if  not re.search(r"[A-Za-z]",password):
        raise ValidationError("Password must contain atleast one alphabet")
    if not re.search(r"[A-Z]",password):
        raise ValidationError("Password must contain atleast one Uppercase character")
    
def validate_age(value):
    if value < 18:
        raise ValidationError("Your age must be grater than 18")
    
def validate_name(value):
    if not re.search(r"^[A-Za-z ]+$",value):
        raise ValidationError('Name cannot contain any special characters')