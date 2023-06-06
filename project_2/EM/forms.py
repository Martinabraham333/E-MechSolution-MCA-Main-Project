from django import forms
from .models import *
from home.models import *



class profile_updateForm(forms.ModelForm):

 
   class Meta:
      model = emprofiles
      fields =['profile_picture','domain','service_place','experience','address','service_charge']
      

class userRegForm(forms.ModelForm):
    class Meta:
        model = Tech_reg
        fields = ['phone']

class TechnicianReply_form(forms.ModelForm):
   class Meta:
      model=TechnicianReply
      fields=['service_request','technician','status','comment']
     
     
class reply_cancel_form(forms.ModelForm):
   class Meta:
      model = CancelReply
      fields =['reason']    

      
from home.models import *
from django import forms

class feedback_form(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['Cl_reg','tech_reg','feedback']   

