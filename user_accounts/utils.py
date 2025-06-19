import random 
from .models import Account

def generate_account_number():
    while True:
        acc_number = str(random.randint(100000,999999))
        if not Account.objects.filter(account_number=acc_number).exists():
            return acc_number