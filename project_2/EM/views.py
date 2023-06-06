from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from home.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .models import Em_history

from django.contrib import messages
from home.models import Tech_reg
from CL.models import *
from django.utils import timezone

# Create your views here.
@login_required
def em_index(request):
    technician = Technicians.objects.get(user=request.user)
    p_dict={
        'p_form':technician.emprofiles,
        'technician':technician
    }
    return render(request, 'em/em_index.html',p_dict)
@login_required
def edit_profile(request):
    place=serv_place.objects.all()
    if request.method== 'POST':
        u_form=userRegForm(request.POST,  instance=request.user.tech_reg)
        technician = Technicians.objects.get(user=request.user)

        p_form= profile_updateForm(request.POST, 
                                 request.FILES, 
                                 instance=technician.emprofiles)
        if p_form.is_valid() and u_form.is_valid() :
            service_place = p_form.cleaned_data['service_place']
            place_obj, created = serv_place.objects.get_or_create(s_place=service_place)


            place_obj.save()
            u_form.save()
            p_form.save() 
            
            #messages.success(request, f'Your profile is updated') 
            return redirect ('em_index')    
    else:
        u_form=userRegForm(instance=request.user.tech_reg)
        technician = Technicians.objects.get(user=request.user)
        p_form= profile_updateForm(instance=technician.emprofiles)
        

    context ={
        'u_form':u_form,
        'p_form':p_form,
        'place':place
    }
    return render (request,'em/edit_profile.html',context)
    

def em_notification(request):
    emNotification=clrequest.objects.all()
    mul_Notification=mul_clrequest.objects.all()
    Cancel=cancel_request.objects.all()
    context={
         'notification':emNotification,
         'mul_Notification':mul_Notification,
         'Cancel':Cancel
         
    }
    return render(request,'em/em_notification.html',context)

def em_contact(request):
    return render(request,'em/em_contact.html')





def reply(request,cl_request_id):
    cl_requestID=get_object_or_404(clrequest,id=cl_request_id)
    technicians=Technicians.objects.get(user=request.user)
    if request.method=="POST":
         
         em_replay=TechnicianReply_form(request.POST)
         status=request.POST['status']
         if em_replay.is_valid():
           
           em_replay_1=em_replay.save(commit=False)
           em_replay_1.service_request=cl_requestID
           em_replay_1.technician=technicians
           em_replay_1.status=status
           em_replay_1.save()
           return redirect('em_history')
    print("Not worked ")       
    em_replay=TechnicianReply_form()
    context={
        
        'em_replay':em_replay
    }
    return render(request,'em/reply.html',context)  


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

 
def cl_request_view(request,notif_id):
    cl_request=get_object_or_404(clrequest,id=notif_id)
    technicians=Technicians.objects.get(user=request.user)
    client=cl_request.cl.user.user_reg
    client_phone=client.phone
    print(client_phone)
    print(technicians.user.username)
    if request.method=="POST":
         
         em_replay_pro=TechnicianReply_form(request.POST)
         status=request.POST['status']
         if em_replay_pro.is_valid():
           
           em_replay_1=em_replay_pro.save(commit=False)
           em_replay_1.service_request=cl_request
           em_replay_1.technician=technicians
           current_time = timezone.now()
           em_replay_1.created_at=current_time
           em_replay_1.status=status
           
           em_replay_1.save()
           if em_replay_1.status == "Accepted":
              cl_request.request_status="Accepted"
              cl_request.em=technicians
              cl_request.save()
           else:
              cl_request.request_status="Rejected"
              cl_request.em=technicians
              cl_request.save()
           print("hello",em_replay_1.id)
           em_history_object = Em_history.objects.create(em_reply=em_replay_1)
           
           em_history_object.save()
           #Remove comment from below two  code to activate text message
           #message = f'Hello User....... { technicians.user.username}  {em_replay_1.status} your Request. REQUEST ID is PRA_{cl_request.id}'
           #send_text_message(client_phone, message)
           message = "You have succesfully Send reply to Service Request"
           response = HttpResponse()
           response['Content-Type'] = 'text/html'
           response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/em/em_history/";
                </script>
            ''')
           return response
           
    em_replay=TechnicianReply_form()
    context={
        'cl_request':cl_request,
        'em_replay':em_replay
    }
    return render(request,'em/cl_request_view.html',context)     

def em_history(request):
    #em_replay=TechnicianReply.objects.all()
    #cancel=CancelReply.objects.all()
    history=Em_history.objects.all()
    context={
        
        #'em_replay':em_replay,
        'history':history
    }
    return render(request,'em/em_history.html',context)

def reply_cancel(request,reply_id):
    if request.method == 'POST':
        
        reply = get_object_or_404(TechnicianReply, id=reply_id)
        cancel_request=reply_cancel_form(request.POST)
        if reply.technician.user == request.user:  # check if the client owns the request
            if cancel_request.is_valid():
              cancel = cancel_request.save(commit=False)
              cancel.em_reply=reply
              cancel.technician = reply.technician
              
              if reply.service_request:  # check if the service request is a clrequest
                      cancel.client = reply.service_request.cl
              elif reply.service_mul_request:  # check if the service request is a mul_clrequest
                      cancel.client = reply.service_mul_request.cl
              current_time = timezone.now()
              cancel.date = current_time
              cancel.save()
              

              if reply.service_mul_request:  # check if the service request is a mul_clrequest
                   reply.service_mul_request.request_status = "Rejected"
                   #reply.service_mul_request.em = reply.technician
                   reply.service_mul_request.save()
              else :
                   reply.service_request.request_status = "Rejected"
                   
                   reply.service_request.save()

            
            reply.status="Canceled"
            reply.save()
            if reply.service_mul_request:
                client=reply.service_mul_request.cl.user.user_reg
                client_phone=client.phone
                #Remove comment from below two  code to activate text message
                #message = f'CANCELED!!!....... { reply.technician.user.username}  Canceled your Request. REQUEST ID is MUL_{reply.service_mul_request.id}. Reason : {cancel.reason} '
                #send_text_message(client_phone, message)

                """if reply.status=="Canceled" and reply.technician.user.username != request.user.username:
                 print(reply.technician.user.username)
                 techs = emprofiles.objects.all()
                 for tech in techs:
                     if tech.service_place == reply.service_mul_request.place and  tech.domain == reply.service_mul_request.domain and tech.get_average_rating() >= reply.service_mul_request.rating :
                          tech_1=tech.em.user.tech_reg
                          tech_phone=tech_1.phone
                          print(tech_phone)
                          message = f'Service-Request from {client.user.username} at {reply.service_mul_request.service_address} Reopend.Please check your Multi Request Alert page.REQUEST ID is MUL_{reply.service_mul_request.id}'
                          send_text_message(tech_phone, message)"""

                    



            else:
                client=reply.service_request.cl.user.user_reg
                client_phone=client.phone
                #Remove comment from below two  code to activate text message
                #message = f'CANCELED!!!....... { reply.technician.user.username}  Canceled your Request. REQUEST ID is PRA_{reply.service_request.id}. Reason : {cancel.reason} '
                #send_text_message(client_phone, message)
            
            em_history_object = Em_history.objects.create(cancel_reply=cancel)
           
            em_history_object.save()
            
           
            message = "You have succesfully canceled Service Request"
            response = HttpResponse()
            response['Content-Type'] = 'text/html'
            response.write(f'''
                    <script>
                        alert("{message}");
                        window.location.href =  "/em/em_history/";
                    </script>
                ''')
            return response
        else:
            
            return redirect('reply_cancel') 
    cancel_reply=reply_cancel_form()
    context={
        
        'cancel_reply':cancel_reply
    }
    return render(request,'em/cancel_reply.html',context)
    #return render(request,'em/cancel_request.html')

def cl_mul_request_view(request,notif_id):
    
    cl_request=get_object_or_404(mul_clrequest,id=notif_id)
    technicians=Technicians.objects.get(user=request.user)
    client=cl_request.cl.user.user_reg
    client_phone=client.phone
    print(client_phone)
    if cl_request.request_status=="Accepted":
          return HttpResponse("You Are Late....! A Technican Already Acceped This Request!!!!.If This Request Canceled By That Technican This request again open")
   
    elif request.method=="POST":
         
         em_replay=TechnicianReply_form(request.POST)
         status=request.POST['status']
         if em_replay.is_valid():
           
           em_replay_1=em_replay.save(commit=False)
           em_replay_1.service_mul_request=cl_request
           em_replay_1.technician=technicians
           current_time = timezone.now()
           em_replay_1.created_at=current_time
           em_replay_1.status=status
           
           em_replay_1.save()
           if em_replay_1.status == "Accepted":
              cl_request.request_status="Accepted"
              cl_request.em=technicians
              cl_request.save()
           else:
              cl_request.request_status="Rejected"
              cl_request.em=technicians
              cl_request.save()
              

           em_history_object = Em_history.objects.create(em_reply=em_replay_1)
           
           em_history_object.save()
           #Remove comment from below two  code to activate text message
           #message = f'Hello User....... { technicians.user.username}  {em_replay_1.status} your Request '
           #send_text_message(client_phone, message)
           message = "You have succesfully Send reply to Service Request"
           response = HttpResponse()
           response['Content-Type'] = 'text/html'
           response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/em/em_history/";
                </script>
            ''')
           return response
    em_replay=TechnicianReply_form()
    context={
        'cl_request':cl_request,
        'em_replay':em_replay
    }
    return render(request,'em/cl_mul_request_view.html',context)   

def reply_view(request,reply_id):
    Reply=get_object_or_404(TechnicianReply,id=reply_id)
    context={
        'Reply':Reply
    }
    return render(request,'em/reply_view.html',context)

def cancel_request_view(request,cancel_id):
    Cancel=get_object_or_404(CancelReply,id=cancel_id)
    
    context={
        'Cancel':Cancel
    }
    return render(request,'em/cancel_view.html',context)




def Multi_Request_alert (request):
    #emNotification=clrequest.objects.all()
    mul_Notification=mul_clrequest.objects.all()
    #Cancel=cancel_request.objects.all()
    context={
         #'notification':emNotification,
         'mul_Notification':mul_Notification
         #'Cancel':Cancel
         
    }
    return render(request,'em/Multi_Request_alert.html',context)   

def Personalized_Request_Alert (request):
    emNotification=clrequest.objects.all()
    #mul_Notification=mul_clrequest.objects.all()
    #Cancel=cancel_request.objects.all()
    context={
         'notification':emNotification
         #'mul_Notification':mul_Notification
         #'Cancel':Cancel
         
    }
    return render(request,'em/Personalized_Request_Alert.html',context) 

def Request_Withdrawal_Notif (request):
    #emNotification=clrequest.objects.all()
    #mul_Notification=mul_clrequest.objects.all()
    Cancel=cancel_request.objects.all()
    context={
         #'notification':emNotification
         #'mul_Notification':mul_Notification
         'Cancel':Cancel
         
    }
    return render(request,'em/Request_Withdrawal_Notif.html',context) 


def pending_work(request):
    work=TechnicianReply.objects.all()
    context={
        'work':work
    }
    return render(request,'em/work.html',context) 

def cl_cancel_view(request,cl_cancel_id):
    Cancel=get_object_or_404(cancel_request,id=cl_cancel_id)
    
    context={
        'Cancel':Cancel
    }
    return render(request,'em/cl_cancel_view.html',context)

def mul_request_view(request,mul_request_id):
    mul_request=get_object_or_404(mul_clrequest,id=mul_request_id)
    context={
        'mul_request':mul_request
    }
    return render(request,'em/mul_request_view.html',context)

def request_view(request,request_id):
    cl_request=get_object_or_404(clrequest,id=request_id)
    
    context={
        'cl_request':cl_request,
       
    }
    return render(request,'em/request_view.html',context) 

def feedback(request):
    if request.method=="POST":
       request_form=feedback_form(request.POST)
    
       if request_form.is_valid():
        
          em_request = request_form.save(commit=False)
        
          tech_reg=request.user.tech_reg # access the Tech_reg instance of the logged-in user
       
          em_request.tech_reg = tech_reg           
          em_request.save()  
          message = "You have succesfully send feedback"
          response = HttpResponse()
          response['Content-Type'] = 'text/html'
          response.write(f'''
                <script>
                    alert("{message}");
                    window.location.href =  "/em/em_feedback/";
                </script>
            ''')
          return response            

    feed=feedback_form()
    context={
    'feed':feed
}
    return render(request,'em/em_feedback.html',context)


