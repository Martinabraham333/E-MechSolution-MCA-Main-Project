from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register_view,name='register_view'),
    path('login',views.login_view,name='login_view'),
    path('about',views.about,name='about'),
    path('home_contact',views.contact,name='home_contact'),
path('logout',views.logout_view,name='logout'),
 path('tech_reg',views.technician_register,name="tech_reg")   ,
 path('approval',views.approval,name="approval")    ,
 path('admin_home',views.admin_home,name="admin_home")  , 
  path('admin_approval',views.admin_approval,name="admin_approval")  , 
   path('admin_clients',views.admin_clients,name="admin_clients")  , 
    path('admin_technicans',views.admin_technicans,name="admin_technicans")  , 
    path('admin_feedback',views.admin_feedback,name="admin_feedback")  , 
    path('technican_remove/<int:tech_id>/',views.technican_remove,name='technican_remove'), 
    path('technican_approved/<int:tech_id>/',views.technican_approved,name='technican_approved'), 
     path('client_remove/<int:cl_id>/',views.client_remove,name='client_remove'),
]
