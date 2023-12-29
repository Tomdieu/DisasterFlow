from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User,Citizen,EmergencyResponder

@receiver(post_save,sender=User)
def create_token_and_notify_other_services(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)
        instance.notify_other_services()


@receiver(post_delete,sender=User)
def delete_token_and_notify_other_services(sender,instance,**kwargs):
    instance.notify_other_services()
    instance.auth_token.delete()