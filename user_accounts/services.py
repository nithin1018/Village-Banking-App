from rest_framework.response import Response
from .models import Transaction,Account
from django.db import transaction as db_transaction

#full transaction logic of the withdraw,deposit and transfer of the amount
def handle_transaction(*,user_account, receiver_account, tran_type, amt, desc=""):
    with db_transaction.atomic():
            txn = Transaction(
                 transaction_type=tran_type,
                 amount=amt,
                 description=desc
            )
            if tran_type == 'withdraw':
                 if user_account.balance < amt:
                      txn.sender = user_account
                      txn.status = 'failed'
                      txn.save()
                      raise ValueError("Insufficient Balance")
                 user_account.balance-=amt
                 txn.sender = user_account
                 txn.status = 'success'
                 user_account.save()
            elif tran_type == 'deposit':
                 user_account.balance+=amt
                 txn.receiver = user_account
                 txn.status = 'success'
                 user_account.save()
            elif tran_type == 'transfer':
                 if not receiver_account:
                      raise ValueError("Reciever account needed for amount transfer")
                 txn.sender = user_account
                 txn.receiver = receiver_account
                 if user_account.balance < amt:
                      txn.status = 'failed'
                      txn.save()
                      raise ValueError("Insufficient Balance")
                 user_account.balance-=amt
                 receiver_account.balance+=amt
                 txn.status = 'success'
                 user_account.save()
                 receiver_account.save()
            else:
                raise ValueError("Invalid transaction type")
            txn.save()
            return txn