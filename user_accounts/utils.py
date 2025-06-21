import random 
from .models import Account
from django.db.models import Sum

def generate_account_number():
    while True:
        acc_number = str(random.randint(1000, 999999))
        if not Account.objects.filter(account_number=acc_number).exists():
            return acc_number
        
def get_account_balance():
    result = Account.objects.aggregate(total=Sum('balance'))
    return result['total'] or 0.00