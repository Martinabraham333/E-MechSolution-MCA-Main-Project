from .models import *
from django import forms

class feedback_form(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['Cl_reg','tech_reg','feedback']


