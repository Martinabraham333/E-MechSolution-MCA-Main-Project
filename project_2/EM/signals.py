from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import emprofiles,Technicians
from home.models import UserType

#if UserType.objects.get(user_id=User.id).type=="Technicians":
@receiver(post_save, sender=Technicians)
def create_profile(sender,instance, created,  **kwargs):
    if created:
        
         emprofiles.objects.create(em=instance)


@receiver(post_save, sender=Technicians)
def save_profile(sender,instance,  **kwargs):

    instance.emprofiles.save()
