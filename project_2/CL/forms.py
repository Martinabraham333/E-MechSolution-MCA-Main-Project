from django import forms
from .models import *
from home.models import user_reg

class update_cl_profile(forms.ModelForm):
   class Meta:
      model = clprofile
      fields =['cl_profile','cl_address','service_place']
      labels={
        'cl_profile':"Profile Picture",
        'cl_address':"Address",
        'service_place':"Preferred Technician Place"
      }

class clrequest_form(forms.ModelForm):
  class Meta:
    model=clrequest
    fields=[
      'cl',
      'em',
    'service_address',
    'complaint',
    'device_image',
    'created_at',
    'date'
    ]
    labels={
      'service_address':"Service Address",
      'complaint':"Complaint About Your Device",
      'device_image':"Device Image"
    }
    widgets={
         'date':forms.DateInput(attrs={'type':'date'})
      }


class Rating_form(forms.ModelForm):
   class Meta:
      model = Rating
      fields =['value','client','technician','review']
     
class request_cancel_form(forms.ModelForm):
   class Meta:
      model = cancel_request
      fields =['reason']
 
class mul_clrequest_form(forms.ModelForm):
  class Meta:
    model=mul_clrequest
    fields=[
      'cl',
    'service_address',
    'complaint',
    'device_image',
    'created_at',
    'date',
    'place',
    'rating',
    'domain',
    'searvice_charge',
    ]
    labels={
      'service_address':"Service Address",
      'complaint':"Complaint About Your Device",
      'device_image':"Device Image"
    }
    widgets={
         'date':forms.DateInput(attrs={'type':'date'})
      }


from home.models import *
from django import forms

class feedback_form(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['Cl_reg','tech_reg','feedback']
