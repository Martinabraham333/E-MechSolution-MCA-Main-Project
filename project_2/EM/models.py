from django.db import models
from CL.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg
from home.models import Tech_reg
current_time = timezone.now()

# Create your models here.

class Technicians(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self) :
        return f'{self.user.username} '

    def get_average_rating(self):
        ratings = Rating.objects.filter(technician=self)
        if ratings.count() > 0:
            return round(ratings.aggregate(Avg('value'))['value__avg'], 1)
        else:
            return 0.0
        

class emprofiles(models.Model):
   
    em = models.OneToOneField(Technicians, on_delete=models.CASCADE,null=True,blank=True)
    profile_picture = models.ImageField( default='default.jpg' ,upload_to='profile_pics')
    domain=models.CharField(max_length=200,null=True,blank=True)
    service_place=models.CharField(max_length=200,null=True,blank=True)
    
    experience=models.IntegerField(null=True,blank=True)
    address=models.TextField(max_length=50)
    service_charge=models.IntegerField(null=True,blank=True)
    #images=models.ImageField(upload_to='profile_images',null=True, blank=True)


    def __str__(self) :
        return f'{self.user.username} Profile'
    def get_average_rating(self):
        return self.em.get_average_rating()

class TechnicianReply(models.Model):
    service_mul_request = models.ForeignKey(mul_clrequest, on_delete=models.CASCADE,null=True,blank=True,related_name='technician_replies')
    service_request = models.ForeignKey(clrequest, on_delete=models.CASCADE,null=True,blank=True)
    technician = models.ForeignKey(Technicians, on_delete=models.CASCADE,null=True,blank=True)
   
    status=models.CharField(max_length=200,null=True,blank=True)
    comment=models.TextField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(default=current_time,null=True,blank=True)
    

  
class CancelReply(models.Model):
    em_reply=models.ForeignKey(TechnicianReply, on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE,null=True,blank=True)
    technician = models.ForeignKey(Technicians, on_delete=models.CASCADE,null=True,blank=True)

    date=models.DateTimeField(default=current_time,null=True,blank=True)
    reason=models.TextField(max_length=500)
    
   
class Em_history(models.Model):
    em_reply=models.ForeignKey(TechnicianReply, on_delete=models.CASCADE,null=True,blank=True)
    cancel_reply = models.ForeignKey(CancelReply, on_delete=models.CASCADE,null=True,blank=True)
    
class serv_place(models.Model):
    s_place=models.CharField(max_length=100)

