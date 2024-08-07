
from django.urls import  include, path
from . import views

urlpatterns = [
        path('',views.ShowLogin, name="login"),
        path('accounts/', include('django.contrib.auth.urls')),       
        path('add_staff',views.add_staff, name="add_staff"),    
        path('check_email_exist',views.check_email_exist, name="check_email_exist"),    
        path('check_username_exist',views.check_username_exist, name="check_username_exist"),    
        path('account_creation_success',views.account_creation_success, name="success_page"),    
        path('add_staff_save',views.add_staff_save, name="add_staff_save"),   
        path('dologin',views.DoLogin, name="DoLogin"),    
        path('logout_user', views.logout_user, name='logout_user'), 

]