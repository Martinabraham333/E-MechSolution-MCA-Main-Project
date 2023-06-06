from django.db import models
from django.contrib.auth.models import User
#from EM.models import Technicians
from django.utils import timezone
import pytz
# Create your models here.
#indian_tz = pytz.timezone('Asia/Kolkata')
#current_time = timezone.now().astimezone(indian_tz)
current_time = timezone.now()
class Clients(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) :
        return f'{self.user.username} '
    
class clprofile(models.Model):
    cl = models.OneToOneField(Clients, on_delete=models.CASCADE,null=True,blank=True)
    cl_profile=models.ImageField( default='default.jpg' ,upload_to='profile_pics')
    cl_address=models.TextField(max_length=500)
    service_place=models.CharField(default="None" ,  max_length=100,null=True,blank=True)
    def __str__(self) :
        return f'{self.user.username} Profile'

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

class clrequest(models.Model):
    cl = models.ForeignKey(Clients, on_delete=models.CASCADE,null=True,blank=True)
    em = models.ForeignKey('EM.Technicians', on_delete=models.CASCADE,null=True,blank=True)
    service_address=models.TextField(max_length=200)
    complaint=models.TextField(max_length=200)
    device_image=models.ImageField( default='default.jpg' ,upload_to='device_pics')
    date=models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(default=current_time,null=True,blank=True)
    request_status=models.CharField(max_length=200,   default="pending",null=True,blank=True)
    
    



class Rating(models.Model):
    value = models.IntegerField()
    client = models.ForeignKey(Clients, on_delete=models.CASCADE,null=True,blank=True)
    technician = models.ForeignKey('EM.Technicians',  on_delete=models.CASCADE,null=True,blank=True)  
    review=models.TextField(max_length=500,null=True,blank=True)



class mul_clrequest(models.Model):
    cl = models.ForeignKey(Clients, on_delete=models.CASCADE,null=True,blank=True)
    em = models.ForeignKey('EM.Technicians',on_delete=models.CASCADE,null=True,blank=True)

    service_address=models.TextField(max_length=200)
    complaint=models.TextField(max_length=200)
    device_image=models.ImageField( default='default.jpg' ,upload_to='device_pics')
    date=models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(default=current_time,null=True,blank=True)
    place=models.CharField(max_length=100,null=True,blank=True)
    rating=models.IntegerField(null=True,blank=True)
    domain=models.CharField(max_length=100,null=True,blank=True)
    request_status=models.CharField(max_length=200,   default="pending",null=True,blank=True)
    searvice_charge=models.IntegerField(null=True,blank=True)

class cancel_request(models.Model):
    service_mul_request = models.ForeignKey(mul_clrequest, on_delete=models.CASCADE,null=True,blank=True)
    service_request = models.ForeignKey(clrequest, on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE,null=True,blank=True)
    technician = models.ForeignKey('EM.Technicians',on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateTimeField(default=current_time,null=True,blank=True)
    reason=models.TextField(max_length=500)

class Cl_history(models.Model):
     service_mul_request = models.ForeignKey(mul_clrequest, on_delete=models.CASCADE,null=True,blank=True)
     service_request = models.ForeignKey(clrequest, on_delete=models.CASCADE,null=True,blank=True)
     cancel_request = models.ForeignKey(cancel_request, on_delete=models.CASCADE,null=True,blank=True)
  