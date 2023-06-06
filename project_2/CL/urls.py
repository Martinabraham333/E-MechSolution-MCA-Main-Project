from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.cl_index,name='cl_index'),
    path('edit_profile/',views.cl_edit_profile,name='cl_edit_profile'),
    path('search_em_profile/',views.search_em_profile,name='search_em_profile'),
    path('cl_request/<int:tech_id>/',views.cl_request,name='cl_request'),
     path('cl_notifications/',views.cl_notification,name='cl_notification'),
      path('contact/',views.contact,name='contact'),
      path('em_view/<int:tech_id>/',views.em_view,name='em_view'),
      path('em_reply_view/<int:reply_id>/',views.em_replay_view,name='em_replay_view'),
      path('rating/<int:technician_id>/',views.rating_view,name='rating_view'),
      path('cl_history/',views.cl_history,name='cl_history'),
      path('request_cancel/<int:request_id>/',views.request_cancel,name='request_cancel'),
      path('feedback/',views.feedback,name='feedback'),
       path('multiple_requ/',views.multiple_requ,name='multiple_requ'),
      #path('mul_request_cancel/<int:mul_request_id>/',views.mul_request_cancel,name='mul_request_cancel'), 
       path('mul_request_view/<int:mul_request_id>/',views.cl_mul_request_view,name='mul_request_view'), 
       path('em_cancel_view/<int:em_cancel_id>/',views.em_cancel_view,name='em_cancel_view'),
       path('request_view/<int:request_id>/',views.request_view,name='request_view'), 
         path('mul_request_cancel/<int:request_id>/',views.mul_request_cancel,name='mul_request_cancel'), 
]