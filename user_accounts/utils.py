import random 
from .models import Account
from django.db.models import Sum
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import threading
from django.contrib.auth.hashers import make_password

def generate_account_number():
    while True:
        acc_number = str(random.randint(1000, 999999))
        if not Account.objects.filter(account_number=acc_number).exists():
            return acc_number
        
def get_account_balance():
    result = Account.objects.aggregate(total=Sum('balance'))
    return result['total'] or 0.00

def generate_otp():
    return str(random.randint(1000,9999))

class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, reciptent_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.reciptent_list = reciptent_list
        threading.Thread.__init__(self)
    def run(self):
        send_mail(
            self.subject,
            self.message, 
            self.from_email, 
            [self.reciptent_list] if isinstance(self.reciptent_list, str) else self.reciptent_list,
            fail_silently=False
            )
    

def send_otp_email(user, action_description):
    otp = generate_otp()
    otp_created = timezone.now()
    user.otp = make_password(otp)
    user.otp_created_time = otp_created
    user.save()
    subject = f"Otp verification for {action_description}"
    message = f"You OTP is {otp} Please Use the otp before 5min. it will expire in 5 minutes"
    EmailThread(subject, message, settings.EMAIL_HOST_USER, [user.email]).start()
