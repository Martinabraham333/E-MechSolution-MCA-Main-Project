from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import clprofile,Clients
from home.models import UserType

@receiver(post_save, sender=Clients)
def create_profile(sender,instance, created,  **kwargs):
    if created:
        
           clprofile.objects.create(cl=instance)


@receiver(post_save, sender=Clients)
def save_profile(sender,instance,  **kwargs):
  
    instance.clprofile.save()