from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from home.models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from EM.models import Technicians
from CL.models import Clients
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home/home.html')
def register_view(request):
    if request.method=="POST":
    #return render(request,'home/register.html')
            print("worked")
            name=request.POST['name']
            username=request.POST['username']
            phone=request.POST['phone']
            email=request.POST['email']
            
            password=request.POST['password']
            password1=request.POST['password1']

            phone_pattern = r'^\+?\d{10,15}$'  # Pattern for a valid phone number (e.g., +91XXXXXXXXXX)
        
            if not re.match(phone_pattern, phone):
                messages.success(request, "Please enter a valid phone number.")
                return render(request, 'home/register.html')
            
            
            if len(name) and len(username) and len(phone) and len(email) and len(password) and len(password1) > 0:

                
                if password==password1:
                  try:
                    if User.objects.filter(email=email).exists():
                        raise IntegrityError("Already existed Email")
                    
                    elif User.objects.filter(username=username).exists():
                        raise IntegrityError("Already existed Username")
                       
                    else:
                        user=User.objects.create_user(first_name=name,email=email,password=password,username=username,last_name='1')
                        user.save()
                        table_user=user_reg()
                        table_user.user=user
                        table_user.phone="+91"+phone
                        table_user.username=user.username
                        table_user.password=user.password
                        table_user.email=user.email
                        table_user.first_name=user.first_name
                        table_user.save()
                        usertype=UserType()
                        usertype.user=user
                        usertype.userReg=table_user
                        usertype.type="Client"
                        usertype.save()
                        
                        if UserType.objects.get(user_id=user.id).type=="Client":
                            client=Clients()
                            client.user=user
                            client.save()
                        
                        if user is None:
                            messages.success(request,"Registration Failed")
                            return redirect(request,'register_view')
                        else:
                          messages.success(request,"You Are Registered Sucessfully")
                          return redirect('login_view')
                  except IntegrityError as e:
                      messages.error(request, str(e))
                      return render(request, 'home/register.html')     #return render(request,'home/login.html',{'message':'sucessfully registered'})
                else:
                    messages.success(request,"Password did not match")
                    return render(request,'home/register.html')
            else:
                    messages.success(request,"All fields are required")
                    return render(request,'home/register.html')
                    
                    

    else:
        print("Not worked")
        return render(request,'home/register.html')

import re

from django.db import IntegrityError
def technician_register(request):
     
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        
        phone = request.POST['phone']
        email = request.POST['email']
      
        id_proof_number = request.POST['id_proof_number']
        id_prof = request.FILES['id_prof']
        password = request.POST['password']
        password1 = request.POST['password1']

        phone_pattern = r'^\+?\d{10,15}$'  # Pattern for a valid phone number (e.g., +91XXXXXXXXXX)
        
        if not re.match(phone_pattern, phone):
            messages.success(request, "Please enter a valid phone number.")
            return render(request, 'home/tech_register.html')
        
        if len(name) and len(username) and len(phone) and len(email)  and len(password) and len(password1) and len(id_proof_number) > 0:
            if password == password1:
              try:  
                if User.objects.filter(email=email).exists():
                    raise IntegrityError("Already existed Email")
                elif User.objects.filter(username=username).exists():
                    raise IntegrityError("Already existed Username")
                
                    
                else:
                    user = User.objects.create_user(
                        first_name=name, email=email, password=password, username=username, last_name='1'
                    )
                    user.phone = phone
                    user.id_proof_number = id_proof_number
                    user.save()
                    
                    tech_reg = Tech_reg()
                    tech_reg.user = user
                    tech_reg.phone = "+91"+phone
                    tech_reg.id_prof = id_prof
                    tech_reg.id_proof_number = id_proof_number
                    
                    tech_reg.username=user.username
                    tech_reg.password=user.password
                    tech_reg.email=user.email
                    tech_reg.first_name=user.first_name
                    tech_reg.save()
                    
                    usertype = UserType()
                    usertype.user = user
                    usertype.techReg=tech_reg
                    usertype.type = "Tech"
                    usertype.save()
                    
                    if UserType.objects.get(user_id=user.id).type == "Tech":
                        technicians = Technicians()
                        technicians.user = user
                        technicians.save()
                        
                    
                    return redirect('approval')
              except IntegrityError as e :
               messages.error(request, str(e))
               return render(request, 'home/tech_register.html')      
            else:
                messages.success(request, "Password did not match.")
                return render(request, 'home/tech_register.html')
        
        else:
            messages.success(request, "All fields are required.")
            return render(request, 'home/tech_register.html')

    return render(request, 'home/tech_register.html')



def login_view(request):
    if request.method=="POST":
     #return render(request,'home/login.html')
     #print(username)
      username=request.POST.get('username')
      password=request.POST.get('password')
      print("a")
      user=authenticate(username=username,password=password)
      print("b")
      if user is not None:
          print("c")
          login(request,user)
          if user.is_superuser:
              return redirect ('admin_home')
          if user.last_name=='1':
              if UserType.objects.get(user_id=user.id).type=="Tech" and Tech_reg.objects.get(user_id=user.id).status=="Accepted" :
                
                return redirect('em_index')
                
              elif UserType.objects.get(user_id=user.id).type=="Client":
                  return redirect('cl_index')
              #elif UserType.objects.get(user_id= user.id).type=="":
              # return redirect('/')
              else:
                  messages.info(request,"invalid Email or Password")
                  return render(request,'home/login.html')
              
          
          else:
              print("d")
              messages.info(request,"invalid Email or Password")
              return render(request,'home/login.html')
      
      else:
           messages.info(request,"invalid Email or Password")
     
           return render(request,'home/login.html')
    else:
        return render(request,'home/login.html')
    
@never_cache         
def logout_view(request):
    logout(request)
    return redirect('home')




def about(request):
    return render(request,'home/about.html')
def contact(request):
    return render(request,'home/contact.html')

def approval(request):
    return render(request,'home/approval.html')

@login_required
def admin_home(request):

    return render(request,'home/admin_home.html')

def admin_technicans(request):
    technicians=Tech_reg.objects.all()
    context={
        'technicians':technicians
    }
    return render(request,'home/admin_technicans.html',context)

def admin_clients(request):

    clients=user_reg.objects.all()
    context={
        'clients':clients
    }
    
    return render(request,'home/admin_clients.html',context)

def admin_approval(request):
    technicians=Tech_reg.objects.all()
    context={
        'technicians':technicians
    }
    return render(request,'home/admin_approval.html',context)

def admin_feedback(request):
    feed=feedback.objects.all()
    context={
       'feed' :feed
    }
    return render(request,'home/admin_feedback.html',context)

def technican_remove(request,tech_id):
    technician = get_object_or_404(Tech_reg, id=tech_id)
    user = technician.user
    technician.delete()
    user.delete()
    
    return redirect('admin_technicans')

def technican_approved(request,tech_id):
    technician = get_object_or_404(Tech_reg, id=tech_id)
    technician.status ="Accepted"
    technician.save()
    return redirect('admin_home')

def client_remove(request,cl_id):
    client = get_object_or_404(user_reg, id=cl_id)
    user = client.user
    client.delete()
    user.delete()
    
    return redirect('admin_clients')

