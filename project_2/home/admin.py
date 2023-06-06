"""from django.contrib import admin

# Register your models here.
from .models import *
#admin.site.register(user_reg)
#admin.site.register(UserType)
#admin.site.register(Tech_reg)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Tech_reg
from django.utils.html import format_html

class Tech_regInline(admin.StackedInline):
    model = Tech_reg
    can_delete = False
    verbose_name_plural = 'Other Details and Approval'
    
class CustomUserAdmin(UserAdmin):
    inlines = (Tech_regInline, )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'id_proof_number','id_prof', 'experience', 'status')
    
    list_select_related = ('tech_reg',)
    
    def phone(self, instance):
        return instance.tech_reg.phone

    def id_proof_number(self, instance):
        return instance.tech_reg.id_proof_number
    
    def experience(self, instance):
        return instance.tech_reg.experience

    def status(self, instance):
        return instance.tech_reg.status
    
    def id_prof(self, instance):
        url = instance.tech_reg.id_prof.url
        return format_html('<a href="{}" target="_blank">View Image</a>'.format(url))

    id_prof.short_description = 'ID Proof'
    
#def id_prof_image(self, instance):
        #return format_html('<img src="{}" width="50"/>'.format(instance.tech_reg.id_prof.url))

    #id_prof_image.short_description = 'ID Proof'
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""
