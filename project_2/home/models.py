from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.

class user_reg(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    phone=models.CharField(max_length=13,blank=False)  
    username = models.CharField(max_length=150,null=True, blank=False)
    password = models.CharField(max_length=128,null=True, blank=False)
    email = models.EmailField(max_length=254,null=True, blank=False)
    first_name = models.CharField(max_length=30,null=True, blank=False)

from django.core.mail import send_mail,EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from twilio.rest import Client
class Tech_reg(models.Model):
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=13, blank=False)
    id_proof_number = models.CharField(max_length=100)
    id_prof = models.ImageField(upload_to='Id_proof_image')
   
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")
    username = models.CharField(max_length=150,null=True, blank=False)
    password = models.CharField(max_length=128,null=True, blank=False)
    email = models.EmailField(max_length=254,null=True, blank=False)
    first_name = models.CharField(max_length=30,null=True, blank=False)

     #technician = models.ForeignKey(Technicians, on_delete=models.CASCADE,null=True,blank=True)

  
    #Remove tripple invorted comma from below codes to enable approval message
    
    """ def send_text_message(self):
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your registration request has been accepted.You can login now in website.All the best!!!!",
            from_='',
            to=self.phone
        )

    def save(self, *args, **kwargs):
        # check if the status has changed to "Accepted"
        if self.id and self.status != Tech_reg.objects.get(pk=self.id).status and self.status == self.ACCEPTED:
            # send the text message
            self.send_text_message()
        super().save(*args, **kwargs)"""




     






class feedback(models.Model):
    Cl_reg=models.ForeignKey(user_reg, on_delete=models.CASCADE,null=True,blank=True)
    tech_reg=models.ForeignKey(Tech_reg, on_delete=models.CASCADE,null=True,blank=True) 
    feedback=models.TextField()

class UserType(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    userReg=models.OneToOneField(user_reg,on_delete=models.CASCADE,null=True,blank=True)
    techReg=models.OneToOneField(Tech_reg,on_delete=models.CASCADE,null=True,blank=True)
    type=models.CharField(max_length=50,blank=False)
