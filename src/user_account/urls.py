from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'User_account'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_template/', views.login_template, name='login_template'),
    path('register_template/', views.register_template, name='register_template'),
    path('loginuser/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('register_tenant', views.register_tenant, name='register_tenant'),
    path('register_landlord', views.register_landlord, name='register_landlord'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)