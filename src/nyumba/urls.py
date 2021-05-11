from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'nyumba'

urlpatterns = [
    #landlord urls
    path('landlord_home/', views.landlord_home, name='landlord_home'),
    path('properties/', views.properties, name='properties'),
    path('individual_property/', views.individual_property, name='individual_property'),
    path('add_property/', views.add_property_form, name='add_property'),
    path('units/', views.units, name='units'),
    path('individual_units/', views.individual_units, name='individual_units'),
    path('add_units/', views.add_units, name='add_Units'),
    path('accounting/', views.accounting, name='accounting'),
    path('balances/', views.balances, name='balances'),
    path('maintenance/', views.maintenance, name='maintenace'),
    path('reminders/', views.reminders, name='reminders'),
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    path('add_maintenance_request', views.add_maintenace_request, name='add_maintenace_request'),
    path('stores/', views.stores, name='stores'),
    path('individual_store/', views.individual_store, name='individual_store'),
    path('store_applications/', views.store_applications, name='store_applications'),
    path('store_application_form/', views.store_application_form, name='store_application_form'),
    path('store_form/', views.store_form, name='store_form'),
    path('tenants/', views.tenants, name='tenants'),
    path('rental_applications/', views.rental_applications, name='rental_applications'),
    path('rental_application_form/', views.rental_application_form, name='rental_application_form'),
    path('profile/', views.landlord_profile, name='profile'),
    #tenant urls
    path('tenant_home/', views.tenant_home, name='tenant_home'),
    #common urls
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)