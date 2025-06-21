from .models import Profile,Account
from .utils import generate_account_number
from django.db.models.signals import post_save
from django.dispatch import receiver

#used to create the account for the Profile when the profile_type is user
@receiver(post_save,sender=Profile)
def create_account_for_new_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'account') and instance.profile_type == 'user':
        Account.objects.create(
            user = instance,
            account_number = generate_account_number()
        )