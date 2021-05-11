from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import *

#landlord views

def landlord_home(request):
    return render(request, 'nyumba/landlord/landlord_home.html')
#properties
def properties(request):
    return render(request, 'nyumba/landlord/properties.html')

def individual_property(request):
    return render(request, 'nyumba/landlord/individual_property.html')
 
def add_property_form(request):
    return render(request, 'nyumba/landlord/add_property.html')
#units
def units(request):
    return render(request, 'nyumba/landlord/units.html')

def individual_units(request):
    return render(request, 'nyumba/landlord/individual_units.html')
def add_units(request):
    return render(request, 'nyumba/landlord/add_units.html')

#accounting and balances
def accounting(request):
    return render(request, 'nyumba/landlord/accounting.html')
def balances(request):
    return render(request, 'nyumba/landlord/balances.html')

#maintenances
def maintenance(request):
    return render(request, 'nyumba/landlord/maintenance.html')
def add_maintenace_request(request):
    return render(request, 'nyumba/landlord/add_maintenance_request.html' )
def reminders(request):
    return render(request, 'nyumba/landlord/reminders.html')

def add_reminder(request):
    return render(request, 'nyumba/landlord/add_reminder.html')

#Stores
def stores(request):
    return render(request, 'nyumba/landlord/stores.html')
def individual_store(request):
    return render(request, 'nyumba/landlord/individual_store.html')
def store_applications(request):
    return render(request,'nyumba/landlord/stores_application.html')
def store_application_form(request):
    return render(request,'nyumba/landlord/store_application_form.html')
def store_form(request):
    return render(request, 'nyumba/landlord/store_form.html')

#Tenants
def tenants(request):
    return render(request, 'nyumba/landlord/tenants.html')
def rental_applications(request):
    return render(request, 'nyumba/landlord/rental_applications.html')
def rental_application_form(request):
    return render(request, 'nyumba/landlord/rental_application_form.html')
    
    
#Reports
def reports(request):
    return render(request, 'nyumba/landlord/reports.html')
#profile
def landlord_profile(request):
    return render(request, 'nyumba/landlord/profile.html')


#tenant views
def tenant_home(request):
    return render(request, 'nyumba/tenant/tenant_home.html')


#common views
@login_required()
def logout_user(request):
	logout(request)
	return redirect('User_account:login')


