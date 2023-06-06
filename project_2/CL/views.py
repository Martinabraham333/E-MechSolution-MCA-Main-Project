from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from home.models import UserType,user_reg
from .models import Clients, clprofile,clrequest
from EM.models import *
from EM.forms import userRegForm,profile_updateForm
from django.db.models import Avg
from django.contrib import messages
from django.utils import timezone


#import pytz
#indian_tz = pytz.timezone('Asia/Kolkata')
#current_time = timezone.now().astimezone(indian_tz)
current_time = timezone.now()
# Create your views here.
@login_required
def cl_index(request):
    client = Clients.objects.get(user=request.user)
    p_dict={
        'p_form':client.clprofile
    }
    
    return render(request,'cl/cl_index.html',p_dict)
@login_required
def cl_edit_profile(request):
    place=serv_place.objects.all()
    if request.method== 'POST':
        u_form=userRegForm(request.POST,  instance=request.user.user_reg)
        client = Clients.objects.get(user=request.user)
        p_form= update_cl_profile(request.POST, 
                                 request.FILES, 
                                 instance=client.clprofile)
        if p_form.is_valid() and u_form.is_valid() :
           
            p_form.save() 
            u_form.save()
            #messages.success(request, f'Your profile is updated') 
            return redirect ('cl_index')    
    else:
       
        client = Clients.objects.get(user=request.user)
        p_form= update_cl_profile(instance=client.clprofile)
        u_form=userRegForm(instance=request.user.user_reg)

    context ={
        
        'p_form':p_form,
        'u_form':u_form,
        'place':place
    }
   
    
    return render(request,'cl/edit_profile.html',context)

@login_required
def search_em_profile(request):
    place=serv_place.objects.all()
    client=Clients.objects.get(user=request.user)
    service_place_query = request.GET.get('service_place','')
    domain_query = request.GET.get('domain','')
    user_query = request.GET.get('em','')
    rating_query= request.GET.get('rating','')
    charge_query=request.GET.get('charge','')
    if service_place_query and domain_query and rating_query and charge_query:
        technicians = Technicians.objects.filter(
            emprofiles__service_place__icontains=service_place_query,
            emprofiles__domain__icontains=domain_query,
            emprofiles__service_charge__lte=charge_query,
        ).annotate(avg_rating=Avg('rating__value')).filter(avg_rating__gte=rating_query)
    
    elif service_place_query  and rating_query and charge_query:
          technicians = Technicians.objects.filter(
            emprofiles__service_place__icontains=service_place_query,
           
            emprofiles__service_charge__lte=charge_query,
        ).annotate(avg_rating=Avg('rating__value')).filter(avg_rating__gte=rating_query)

    elif  service_place_query and domain_query and charge_query:
           technicians = Technicians.objects.filter(
           
            emprofiles__service_place__icontains=service_place_query,
             emprofiles__domain__icontains=domain_query,
             emprofiles__service_charge__icontains=charge_query,
        )
           
    elif rating_query:
         technicians = Technicians.objects.filter().annotate(avg_rating=Avg('rating__value')).filter(avg_rating__gte=rating_query)
    
    elif service_place_query:
        technicians = Technicians.objects.filter(
            emprofiles__service_place__icontains=service_place_query
        )
    elif domain_query:
        technicians = Technicians.objects.filter(
            emprofiles__domain__icontains=domain_query
        )
    elif user_query:
        technicians = Technicians.objects.filter(
            user__username__icontains=user_query
        )
    elif charge_query:
      if charge_query:
        technicians = Technicians.objects.filter(
           emprofiles__service_charge__lte=charge_query
        )
  
    else:
        technicians = Technicians.objects.filter(
            emprofiles__service_place__icontains=client.clprofile.service_place
        )
    
    
    context = {
        'technicians': technicians,
        'service_place_query': service_place_query,
        'domain_query': domain_query,
        'user_query':user_query,
        'rating_query': rating_query,
        'charge_query':charge_query,
        'place':place
    }
    return render(request,'cl/search_em_profile.html',context )

def em_view(request, tech_id):
    print(tech_id)
    technician = get_object_or_404(Technicians, id=tech_id)
    ratings = Rating.objects.filter(technician=technician)
    avg_rating = ratings.aggregate(Avg('value'))['value__avg']
    if avg_rating is not None:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0.0
    count_rating = ratings.count()
    context = {
        'technician': technician,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'count_rating': count_rating
    }
    return render(request, 'cl/em_view.html', context)





from twilio.rest import Client
def send_text_message(to_number, message):
    # Your Twilio API credentials
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    
    # Send the message
    message = client.messages.create(
        to=to_number,
        from_='',  # Your Twilio phone number
        body=message)
    return message.sid




def cl_request(request,tech_id):
    technician=get_object_or_404(Technicians,id=tech_id)
    client = Clients.objects.get(user=request.user)
    tech=technician.user.tech_reg
    tech_phone=tech.phone
    print(tech_phone)
    if request.method=="POST":
        request_form=clrequest_form(request.POST,request.FILES)
        
        if request_form.is_valid():
            cl_request = request_form.save(commit=False)
            cl_request.em= technician
            cl_request.cl=client
            cl_request.created_at= timezone.now()
            cl_request.save()
            cl_history_object = Cl_history.objects.create(service_request=cl_request)
           
            cl_history_object.save()
            #Remove comment from below two code to activate text message
            #message = f'New Personalised Service request from {client.user.username} at {cl_request.service_address}.Chech your Personalised Request Alert page.REQUEST ID is PRA_{cl_request.id}'
            #send_text_message(tech_phone, message)
         
            message = "You Have Succesfully Send Service Request"
            response = HttpResponse()
            response['Content-Type'] = 'text/html'
            response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/cl/cl_history/";
                </script>
            ''')
            return response
    request_form=clrequest_form()
    context={
        'request_form':request_form,
        'technician': technician
    }
    return render(request,'cl/cl_request.html',context)

def cl_notification(request):
    notif=Em_history.objects.all()
    context={
        'notif':notif
    }
    return render(request,'cl/notifications.html',context)

def em_replay_view(request,reply_id):
    Reply=get_object_or_404(TechnicianReply,id=reply_id)
    context={
        'Reply':Reply
    }
    return render(request,'cl/em_reply_view.html',context)

def rating_view(request,technician_id):
    technician=get_object_or_404(Technicians,id=technician_id)
    client=Clients.objects.get(user=request.user)
    try:
        rating = Rating.objects.get(client=client, technician=technician)
    except Rating.DoesNotExist:
        rating = Rating(client=client, technician=technician)

    
    if request.method=="POST":
          
          rating=Rating_form(request.POST,instance=rating)
          

          
          if rating.is_valid():
            a = rating.cleaned_data.get('value')
            if a >5:
               messages.success(request,"Rating Cannot be greater than 5")
               return redirect('rating_view' ,technician_id)
            else:
               rate=rating.save(commit=False)
               rate.client=client
               rate.technician=technician
               rate.save()
               return redirect('search_em_profile')
    else:
        client=Clients.objects.get(user=request.user)
        rating_form=Rating_form(instance=rating)
        context={

         'technicians':technician,
         'rating_form':rating_form
       }
        return render(request,'cl/rating.html',context)

def contact(request):
    return render(request,'cl/contact.html')

def cl_history(request):
   
    history=Cl_history.objects.all()
    context={
        
        
        'history':history,
    }
    
    return render(request,'cl/cl_history.html',context)

def request_cancel(request,request_id):
    req = get_object_or_404(clrequest, id=request_id)
    tech=req.em.user.tech_reg
    tech_phone=tech.phone
    print(tech_phone)
    if request.method == 'POST':
        
        req = get_object_or_404(clrequest, id=request_id)
        
        cancel_request=request_cancel_form(request.POST)
        if req.cl.user == request.user:  # check if the client owns the request
            if cancel_request.is_valid():
              cancel = cancel_request.save(commit=False)
              cancel.service_request=req
              cancel.technician = req.em
              cancel.client = req.cl
              cancel.date = timezone.now()
              cancel.save()
              
            req.request_status="Canceled"
            req.save()
            cl_history_object = Cl_history.objects.create(cancel_request=cancel)
           
            cl_history_object.save()
            #Remove comment from below two  code to activate text message
            #message = f'Sorry...{ cancel.client} canceled Request '
            #send_text_message(tech_phone, message)
            
            message = "You have Succesfully Cancel the Service Request"
            response = HttpResponse()
            response['Content-Type'] = 'text/html'
            response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/cl/cl_history/";
                </script>
            ''')
            return response
        else:
           
            return redirect('cl_history') 
    cancel_request=request_cancel_form()

    context={
        
        'cancel_request':cancel_request
    }
    return render(request,'cl/cancel_request.html',context)
    


def multiple_requ(request):
    place=serv_place.objects.all()
    client = Clients.objects.get(user=request.user)
    
    
  
    if request.method=="POST":
        request_form=mul_clrequest_form(request.POST,request.FILES)
        
        if request_form.is_valid():
            
                cl_request = request_form.save(commit=False)
                
                cl_request.cl = client
                cl_request.created_at = timezone.now()
                cl_request.save()

                cl_history_object = Cl_history.objects.create(service_mul_request=cl_request)
           
                cl_history_object.save()

                # send notification to all registered technicians
                techs = emprofiles.objects.all()
                for tech in techs:
                     if tech.service_place == cl_request.place and  tech.service_charge <= cl_request.searvice_charge and tech.get_average_rating() >= cl_request.rating :
                          tech_1=tech.em.user.tech_reg
                          tech_phon=tech_1.phone
                          #Remove comment from below two  code to activate text message
                          #message = f'New Multi Service-Request from {client.user.username} at {cl_request.service_address}.Please note that only one technician can accept this request, so please check your Multi Request Alert page.REQUEST ID is MUL_{cl_request.id}'
                          #send_text_message(tech_phon, message)




                message = "You have Succesfully send the Service Request"
                response = HttpResponse()
                response['Content-Type'] = 'text/html'
                response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/cl/cl_history/";
                </script>
            ''')
                return response
    request_form=mul_clrequest_form()
    context={
        'request_form':request_form,
       
        'place':place,
        
    }
    return render(request,'cl/multi_request.html',context)




def cl_mul_request_view(request,mul_request_id):
    mul_request=get_object_or_404(mul_clrequest,id=mul_request_id)
    context={
        'mul_request':mul_request
    }
    return render(request,'cl/mul_request_view.html',context)

def em_cancel_view(request,em_cancel_id):
    Cancel=get_object_or_404(CancelReply,id=em_cancel_id)
    context={
        'Cancel':Cancel
    }
    return render(request,'cl/em_cancel_view.html',context)

def request_view(request,request_id):
    cl_request=get_object_or_404(clrequest,id=request_id)
    
    context={
        'cl_request':cl_request,
       
    }
    return render(request,'cl/request_view.html',context)   


def mul_request_cancel(request,request_id):
    
    if request.method == 'POST':
        
        req = get_object_or_404(mul_clrequest, id=request_id)
       
        cancel_request=request_cancel_form(request.POST)
        if req.cl.user == request.user:  # check if the client owns the request
            if cancel_request.is_valid():
              cancel = cancel_request.save(commit=False)
              cancel.service_mul_request=req
              cancel.technician = req.em
              cancel.client = req.cl
              cancel.date = timezone.now()
              cancel.save()
            
            req.request_status="Canceled"
            req.save()
            cl_history_object = Cl_history.objects.create(cancel_request=cancel)
           
            cl_history_object.save()
            if req.em is not None and req.em.user is not None and req.em.user.tech_reg is not None:
   
              tech=req.em.user.tech_reg
              tech_phone=tech.phone
              #Remove comment from below two  code to activate text message
              #message = f'Sorry...{ cancel.client} canceled Request '
              #send_text_message(tech_phone, message)
              
              message = "You have Succesfully Cancel the Service Request"
              response = HttpResponse()
              response['Content-Type'] = 'text/html'
              response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/cl/cl_history/";
                </script>
            ''')
              return response
            else:
              message = "You have Succesfully Cancel the Service Request"
              response = HttpResponse()
              response['Content-Type'] = 'text/html'
              response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/cl/cl_history/";
                </script>
            ''')
              return response 
        else:
            
            return redirect('cl_history') 
    cancel_request=request_cancel_form()

    context={
        
        'cancel_request':cancel_request
    }
    return render(request,'cl/cancel_request.html',context)


def feedback(request):
    if request.method=="POST":
        request_form=feedback_form(request.POST)
        
        if request_form.is_valid():
            
                cl_request = request_form.save(commit=False)
                print(request.user.user_reg.id)
                reg=request.user.user_reg
                cl=user_reg.objects.get(id=reg.id)
                cl_request.Cl_reg = cl               
                cl_request.save()               
                message = "You have succesfully send feedback"
                response = HttpResponse()
                response['Content-Type'] = 'text/html'
                response.write(f'''
                    <script>
                        alert("{message}");
                        window.location.href =  "/cl/feedback/";
                    </script>
                ''')
                return response   
    feed=feedback_form()
    context={
        'feed':feed
    }
    return render(request,'cl/cl_feedback.html',context)