from django.urls import path,include
from .import views


urlpatterns = [
    
    path('',views.em_index,name='em_index'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
     path('em_notifications/',views.em_notification,name='em_notification'),
      path('em_contact/',views.em_contact,name='em_contact'),
      path('reply/<int:cl_request_id>/',views.reply,name='reply'),
      path('cl_request_view/<int:notif_id>/',views.cl_request_view,name='cl_request_view'),
      path('em_history/',views.em_history,name='em_history'),
      path('reply_cancel/<int:reply_id>/',views.reply_cancel,name='reply_cancel'),
      path('cl_mul_request_view/<int:notif_id>/',views.cl_mul_request_view,name='cl_mul_request_view'),
        path('reply_view/<int:reply_id>/',views.reply_view,name='reply_view'),
         path('cancel_request_view/<int:cancel_id>/',views.cancel_request_view,name='cancel_request_view'),

         path('Request_Withdrawal_Notif/',views.Request_Withdrawal_Notif,name='Request_Withdrawal_Notif'),
         path('Personalized_Request_Alert/',views.Personalized_Request_Alert,name='Personalized_Request_Alert'),
         path('Multi_Request_alert/',views.Multi_Request_alert,name='Multi_Request_alert'),
          path('pending_work/',views.pending_work,name='pending_work'),
          path('cl_cancel_view/<int:cl_cancel_id>/',views.cl_cancel_view,name='cl_cancel_view'),


           path('request_view/<int:mul_request_id>/',views.mul_request_view,name='Mul_request_view'), 
       
       path('request_view/<int:request_id>/',views.request_view,name='Request_view'), 

       path('em_feedback/',views.feedback,name='em_feedback'),


       
]
