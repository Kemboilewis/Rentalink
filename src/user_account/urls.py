from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'user_account'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_template/', views.login_template, name='login_template'),
    path('register_template/', views.register_template, name='register_template'),
    path('loginuser/', views.loginuser, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    #path('register_landlord', views.register_landlord, name='register_landlord'),
    
]