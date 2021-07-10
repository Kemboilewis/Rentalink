from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'nyumba'

urlpatterns = [
    #landlord urls
    path('landlord_home/', views.landlord_home, name='landlord_home'),
    path('properties/', views.properties, name='properties'),
    path('individual_property/<int:plotid>', views.individual_property, name='individual_property'),
    path('property_units/<int:plotid>', views.property_units, name='property_units'),
    path('add_property/', views.add_property_form, name='add_property'),
    path('units/', views.units, name='units'),
    path('individual_units/<int:unitId>', views.individual_units, name='individual_units'),
    path('add_units/', views.add_units, name='add_Units'),
    path('addroom/', views.addroom, name='addroom'),
    path('accounting/', views.accounting, name='accounting'),
    path('balances/', views.balances, name='balances'),
    path('maintenance/', views.maintenance, name='maintenace'),
    path('reminders/', views.reminders, name='reminders'),
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    path('add_maintenance_request', views.add_maintenace_request, name='add_maintenace_request'),
    path('apply_maintenance/', views.apply_maintenance, name='apply_maintenance'),
    path('stores/', views.stores, name='stores'),
    path('individual_store/<int:storeId>', views.individual_store, name='individual_store'),
    path('store_applications/', views.store_applications, name='store_applications'),
    path('store_application_form/', views.store_application_form, name='store_application_form'),
    path('store_form/', views.store_form, name='store_form'),
    path('addstore/', views.addstore, name='addstore'),
    path('request/', views.add_store_application, name="add_store_application"),
    path('storeApp_reply/', views.storeApp_reply, name="storeApp_reply"),
    path('tenants/', views.tenants, name='tenants'),
    path('add_tenant/', views.add_tenant, name='add_tenant'),
    path('register_tenant/', views.add_new_tenant, name='register_tenant'),
    path('tenantinfo/', views.tenantinfo, name='tenantinfo'),
    path('rental_applications/', views.rental_applications, name='rental_applications'),
    path('landlord_reponse/', views.landlord_reponse, name='landlord_reponse'),
    path('rental_application_form/', views.rental_application_form, name='rental_application_form'),
    path('newrentalapp/', views.new_rental_app, name="new_rental_app"),
    path('profile/', views.landlord_profile, name='profile'),
    path('base/', views.base, name='base'),
    path('reports/', views.reports, name='reports'), 
    #### .................landlords action pages...........
    path('addproperty/', views.add_property, name='addproperty'),
    path('paymentreports/', views.printreport, name='paymentreport'),
    path('maintenancechoice/', views.maintenance_choice, name='maintenance_choice'),

    #tenant urls
    path('tenant_home/', views.tenant_home, name='tenant_home'),
    path('explore_rentals', views.explore_rentals, name='explore_rentals'),
    path('houseform/<int:hid>', views.house_form, name='houseform'),
    path('renter_profile/', views.renter_profile, name='renter_profile'),
    path('rental_home/', views.rental_home, name='rental_home'),
    path('myapplications/', views.myapplications, name='myapplications'),
    path('mymaintenance/', views.mymaintenance, name='mymaintenance'),
    path('explore_stores', views.explore_stores, name='explore_stores'),
    path('store_app/<int:storeId>', views.store_app, name='store_app'),
    path('my_messages/', views.my_messages, name='my_messages'),
    path('tenant_profile/', views.tenant_profile, name='tenant_profile'),
    path('menu/', views.menu, name='menu'),
    path('tenantbase/', views.tenantbase, name="tenantbase"),
    path('mystoreapplications/', views.mystoreapplications, name='mystoreapplications'),
    path('printreceipt/<int:rid>', views.print_receipt, name="printreceipt"),#print receipt
    path('transactions/', views.tenant_transactions, name="tenantTransactions"),
    path('TenantbookingStore/', views.Tenant_bookingStore, name='TenantbookingStore'),
    path('tenantmainForm/', views.tenant_mainForm, name='tenantmainForm'),
    path('tenantmaintenance/', views.tenant_maintenance, name='tenantmaintenance'),
    #common urls
    path('chats/', views.inbox, name='inbox'),
    
]