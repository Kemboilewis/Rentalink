from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse#json response
from django.core import serializers #serializing
from django.forms.models import model_to_dict #printing
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
import datetime
from django.contrib import messages
from .models import *
from MpesaPayments.models import *
from user_account.models import myUser

#landlord views
@login_required()
def landlord_home(request):
    return render(request, 'nyumba/landlord/landlord_home.html')
#properties
@login_required()
def properties(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    myplots = Plot.objects.filter(plot_owner=user).order_by('-date_created')
    return render(request, 'nyumba/landlord/properties.html', {'myplots':myplots,})
@login_required()
def individual_property(request,plotid ):
    this_plot=Plot.objects.get(id=plotid)
    i_payments=Succesful_Room_payments.objects.filter(Paid_booking__booked_plot=this_plot)
    i_tenants=Room.objects.filter(room_plot=this_plot,room_status=True)
    count_tenants=Room.objects.filter(room_plot=this_plot,room_status=True).count()
    count_units = Room.objects.filter(room_plot=this_plot).count()
    occupied_units = Room.objects.filter(room_plot=this_plot, room_status=True).count()
    vacant_units = Room.objects.filter(room_plot=this_plot, room_status=False).count()
    count_m= Maintenance.objects.filter(plot=this_plot).count()
    return render(request, 'nyumba/landlord/individual_property.html', {'this_plot':this_plot, 
     'count_units':count_units, 'occupied_units':occupied_units, 'vacant_units':vacant_units,'i_payments':i_payments,
     'i_tenants':i_tenants, 'count_tenants':count_tenants,'count_m':count_m} )

@login_required()
def property_units(request,plotid ):
    current_plot=Plot.objects.get(id=plotid)
    all_units = Room.objects.filter(room_plot=current_plot)
    return render(request, 'nyumba/landlord/property_units.html', {'current_plot':current_plot, 'all_units':all_units})
@login_required()
def add_property_form(request):
    return render(request, 'nyumba/landlord/add_property.html')

# ..................properties action pages .................. 
@login_required()
def add_property(request):
    if request.method == 'POST':
        username = request.user.username
        plot_owner = myUser.objects.get(username=username)
        property_type = request.POST['property_type']
        property_name = request.POST['plot_name']
        year_built = request.POST['year_built']
        location = request.POST['location']
        street_address = request.POST['s_address']
        city = request.POST['city']
        country = request.POST['country']
        property_image = request.FILES.get('property_image', False)
        currency = request.POST['currency'] 
        new=Plot(plot_owner=plot_owner, property_name=property_name, property_type=property_type, year_built=year_built,
         location=location, street_address=street_address, city=city, country=country, property_image=property_image,currency=currency)
  
        try:
            new.save()
        except:
            messages(request, "unable to create the property, Please try again")
            return redirect("nyumba:add_property")
        if property_type == 'single':
            room_plot = new
            room_name = property_name
            room_image = property_image
            beds = request.POST['beds']
            baths = request.POST['baths']
            size = request.POST['size']
            market_rent = request.POST['rent']
            parking = request.POST['parking']
            min_deposit = request.POST['deposit']
            r = Room(room_plot=room_plot, room_name=room_name, room_image= room_image, room_status=False, 
            beds=beds, baths=baths, size=size, market_rent=market_rent, parking=parking, min_deposit=min_deposit)
            try:
                r.save()
                messages.success(request, "property created succesfully")
                return redirect("nyumba:properties")
            except:
                messages.warning(request,"unable to create property, please try again!!!")
                return redirect("nyumba:add_property")
        
        else:
            room_plot = new
            room_name = request.POST['r_name']
            room_image = request.FILES.get('r_image', False)
            beds = request.POST['r_beds']
            baths = request.POST['r_baths']
            size = request.POST['r_size']
            market_rent = request.POST['r_rent']
            parking = request.POST['r_parking']
            min_deposit = request.POST['r_deposit']
            u = Room(room_plot=room_plot, room_name=room_name, room_image= room_image, room_status=False, 
            beds=beds, baths=baths, size=size, market_rent=market_rent, parking=parking, min_deposit=min_deposit)
            try:
                u.save()
                messages.success(request, "property created succesfully")
                return redirect("nyumba:units")
            except:
                messages.warning(request,"unable to create property, please try again!!!")
                return redirect("nyumba:add_property")
    return render(request, 'nyumba/landlord/add_property.html')

@login_required()        
def addroom(request):
    if request.method == 'POST':
        username = request.user.username
        room_tenant = myUser.objects.get(username=username)
        plot_id = request.POST['plot']
        room_plot = Plot.objects.get(id=plot_id)
        room_name = request.POST['unit_name']
        room_image = request.FILES.get('unit_img', False)
        beds = request.POST['beds']
        baths = request.POST['baths']
        size = request.POST['size']
        market_rent = request.POST['rent']
        parking = request.POST['parking']
        min_deposit = request.POST['deposit']
        newr = Room(room_plot=room_plot, room_name=room_name, room_image= room_image, room_status=False, 
        beds=beds, baths=baths, size=size, market_rent=market_rent, parking=parking, min_deposit=min_deposit)
        try:
            newr.save()
            messages.success(request, "unit created succesfully")
            return redirect("nyumba:units")
        except:
            messages.warning(request,"unable to create unit, please try again!!!")
            return redirect("nyumba:addroom")
    return render(request, 'nyumba/landlord/add_units.html')
            

###................end.....................        
####..............stores action page..........
@login_required()        
def addstore(request):
    if request.method == 'POST':
        username = request.user.username
        store_owner = myUser.objects.get(username=username)
        store_name  = request.POST['store_name']
        store_capacity =request.POST['no_units']
        store_image = request.FILES.get('store_img', False) 
        plot_id = request.POST['plot']
        store_plot = Plot.objects.get(id=plot_id)
        store_location = request.POST['store_location']
        year_built = request.POST['year_built']
        store_address = request.POST['address']
        store_state = request.POST['state']

        newstore= Store(store_owner=store_owner, store_name=store_name, store_capacity=store_capacity, store_image=store_image,
        store_plot=store_plot, store_location=store_location, year_built=year_built, store_address=store_address, store_state=store_state)
        try:
            newstore.save()
        except:
            messages.warning(request, 'The creation of the store failes!!! try again')
            return redirect("nyumba:store_form")
        no_units = 0
        no_units = int(store_capacity)
        for i in range(no_units):
            unit_store = newstore
            print(i)
            unit_status = True
            unit_number = i+1
            k=Store_unit(unit_store=unit_store, unit_status=unit_status, unit_number=unit_number)
            try:
                k.save()
            except:
                messages.warning(request, 'Creation of store units failed, contact admin!!')
                return redirect("nyumba:store_form")
        messages.success(request, "succesfully created store and store units")
        return redirect("nyumba:stores")
    return render(request, 'nyumba/landlord/store_form.html')

def add_store_application(request): 
    if request.method == 'POST':
        user_id = request.user.id
        user = myUser.objects.get(id=user_id)
        unit_id = request.POST['unitid']
        applied_unit = Store_unit.objects.get(id=unit_id)
        applied_store = applied_unit.unit_store 
        applying_user = user
        #payment_status = False
        #applied_store 
        starting_date = request.POST['s_date']
        ending_date = request.POST['e_date']
        application_time = datetime.datetime.now()
        new_app = Store_applications(applied_unit=applied_unit, applying_user=applying_user, applied_store=applied_store, 
        starting_date=starting_date, ending_date=ending_date, application_time=application_time)

        try:
            new_app.save()
            messages.success(request, "application send succesfully")
            return redirect("nyumba:store_applications")
        except:
            messages.warning(request, "application failed, try again!!")
            return redirect("nyumba:store_application_form")
    return render(request, 'nyumba/landlord/store_application_form.html')
def storeApp_reply(request):
    if request.method == 'POST':
        app_id = request.POST['applicationId']
        app = Store_applications.objects.get(id=app_id)
        app_unit = app.applied_unit
        choice = request.POST['choice']
        try:
            app.owner_response = choice
            app.save()   
        except:
            messages.warning(request, "response failed, Try again!!")
            return redirect("nyumba:store_applications")
        if choice == "1":
            app_unit.unit_status = False
            app_unit.save()
            messages.success(request,"response send succesfully")
            return redirect("nyumba:store_applications")
    return render(request, 'nyumba/landlord/stores_application.html')

@login_required
def printreport(request):
    user=request.user
    report=Succesful_Room_payments.objects.filter(Paid_booking__booked_plot__plot_owner=user, 
    Paid_booking__payment_status=True)
    total=0
    for k in report:
        total=k.Amount+total
    template_path = 'nyumba/report.html'
    context = {'report': report, 'total':total}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>') 
    return response

#@csrf_exempt
def maintenance_choice(request):
    if request.method == 'POST':
        app_id = request.POST['applicationId']
        app = Maintenance.objects.get(id=app_id)
        #app_unit = app.applied_unit
        choice = request.POST['choice']
        try:
            app.status = choice
            app.save()
            messages.success(request, "response succesfully send!!") 
            return redirect("nyumba:maintenace")  
        except:
            messages.warning(request, "response failed, Try again!!")
            return redirect("nyumba:maintenace")
        # if choice == "1":
        #     app_unit.unit_status = False
        #     app_unit.save()
        #     messages.success(request,"response send succesfully")
        #     return redirect("nyumba:store_applications")
    return render(request, 'nyumba/landlord/stores_application.html')



   
    # .......................end................
#units
@login_required()
def units(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    myunits = Room.objects.filter(room_plot__plot_owner=user, room_plot__property_type='multi_unit')
    return render(request, 'nyumba/landlord/units.html', {'myunits':myunits})
@login_required()
def individual_units(request, unitId):
    this_unit=Room.objects.get(id=unitId)
    u_payments=Succesful_Room_payments.objects.filter(Paid_booking__booked_room=this_unit)
    return render(request, 'nyumba/landlord/individual_units.html', {'this_unit':this_unit,'u_payments':u_payments})
@login_required()
def add_units(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    plots = Plot.objects.filter(plot_owner=user, property_type='multi_unit')
    return render(request, 'nyumba/landlord/add_units.html', {'plots':plots,})

#accounting and balances
@login_required()
def accounting(request):
    user=request.user
    payments=Succesful_Room_payments.objects.filter(Paid_booking__booked_plot__plot_owner=user, Paid_booking__payment_status=True)
    total=0
    for k in payments:
        total=k.Amount+total
    return render(request, 'nyumba/landlord/accounting.html', {'total':total, 'payments':payments})
@login_required()
def balances(request):
    return render(request, 'nyumba/landlord/balances.html')

#maintenances
@login_required()
def maintenance(request):
    user = request.user
    all_applications=Maintenance.objects.filter(plot__plot_owner=user)
    new_r = Maintenance.objects.filter(plot__plot_owner=user, status=0)
    new = Maintenance.objects.filter(plot__plot_owner=user, status=0).count()
    progress = Maintenance.objects.filter(plot__plot_owner=user, status=1).count()
    complete = Maintenance.objects.filter(plot__plot_owner=user, status=2).count()
    return render(request, 'nyumba/landlord/maintenance.html',{'new':new, 'new_r':new_r, 
    'progress':progress, 'complete':complete,'all_applications':all_applications})
@login_required()
def add_maintenace_request(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    user_property = Plot.objects.filter(plot_owner=user)
    user_units = Room.objects.filter(room_plot__plot_owner=user)
    return render(request, 'nyumba/landlord/add_maintenance_request.html',{'user_property':user_property, 'user_units':user_units} )
# ...........maintenance request action views ..................
def apply_maintenance(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = myUser.objects.get(id=user_id)
        applying_user = user
        unit_id = request.POST['unitId']
        unit =  Room.objects.get(id=unit_id)
        unit_plot = unit.room_plot
        subject = request.POST['subject']
        problem = request.POST['problem']
        pro_image = request.FILES.get('pro_image', False)
        new_m =Maintenance(applying_user=applying_user, plot=unit_plot, room=unit, subject=subject, problem=problem, pr_image=pro_image)
        try:
            new_m.save()
            messages.success(request, "you request has been send succesfully")
            return redirect("nyumba:maintenace")
        except:
            messages.warning(request, "you request has failed!! please try again")
            return redirect("nyumba:add_maintenace_request")
    return render(request, 'nyumba/landlord/add_maintenance_request.html.html')

        # plot = 
        # room = 
        # subject = 
        # problem = 
        # pr_image = 
# .........................end..............
@login_required()
def reminders(request):
    return render(request, 'nyumba/landlord/reminders.html')

@login_required()
def add_reminder(request):
    return render(request, 'nyumba/landlord/add_reminder.html')

#Stores
@login_required()
def stores(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    mystores = Store.objects.filter(store_owner=user)

    return render(request, 'nyumba/landlord/stores.html', {'mystores':mystores})
@login_required()
def individual_store(request, storeId):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    current_store=Store.objects.get(id=storeId)
    occupied_units = Store_unit.objects.filter(unit_store=current_store, unit_status=False)
    vacant_units = Store_unit.objects.filter(unit_store=current_store, unit_status=True).count
    stored_mzigo = Store_applications.objects.filter(applied_store__store_owner=user, owner_response="1")
    all_units = Store_unit.objects.filter(unit_store=current_store).count()
    return render(request, 'nyumba/landlord/individual_store.html', {'current_store':current_store, 
    'vacant_units':vacant_units, 'all_units':all_units, 'occupied_units':occupied_units,'stored_mzigo':stored_mzigo})
@login_required()
def store_applications(request):
    all_applications = Store_applications.objects.all()
    return render(request,'nyumba/landlord/stores_application.html', {'all_applications':all_applications})
@login_required()
def store_application_form(request): 
    all_stores = Store.objects.all()
    all_units = Store_unit.objects.all()
    return render(request,'nyumba/landlord/store_application_form.html', {'all_stores':all_stores, 'all_units':all_units})
@login_required()
def store_form(request):
    user_id = request.user.id
    user = myUser.objects.get(id=user_id)
    plots = Plot.objects.filter(plot_owner=user)
    return render(request, 'nyumba/landlord/store_form.html', {'plots':plots})

#Tenants
@login_required()
def tenants(request):
    user = request.user
    #user = myUser.objects.get(id=user_id)
    all_tenants = Room.objects.filter(room_plot__plot_owner=user, room_status=True)
    return render(request, 'nyumba/landlord/tenants.html', {'all_tenants':all_tenants})
@login_required()
def rental_applications(request):
    user = request.user
    a_payments = Succesful_Room_payments.objects.filter(Paid_booking__booked_plot__plot_owner=user)
    all_applications = Room_application.objects.filter(booked_plot__plot_owner=user)
    return render(request, 'nyumba/landlord/rental_applications.html', {'all_applications':all_applications,'a_payments':a_payments})
@login_required()
def rental_application_form(request):
    user=request.user
    list_tenants = myUser.objects.filter(is_tenant=True)
    plots=Plot.objects.filter(plot_owner=user)
    units=Room.objects.filter(room_plot__plot_owner=user, room_status=False)
    return render(request, 'nyumba/landlord/rental_application_form.html', 
    {'plots':plots, 'units':units,'list_tenants':list_tenants})

@login_required()
def add_tenant(request):
    user=request.user
    list_tenants = myUser.objects.filter(is_tenant=True)
    plots=Plot.objects.filter(plot_owner=user)
    units=Room.objects.filter(room_plot__plot_owner=user, room_status=False)
    return render(request, 'nyumba/landlord/add_tenant.html', {'plots':plots, 'units':units,'list_tenants':list_tenants})
# ............tenants action view..........
@login_required
def new_rental_app(request):
    if request.method == 'POST':
        t_id = request.POST['tenant']
        booking_user = myUser.objects.get(id=t_id)
        u_id = request.POST['unitid']
        booked_room = Room.objects.get(id=u_id)
        booked_plot = booked_room.room_plot
        #landlords_response = 1
        # payment_status = False
        #disabled_status = False
        #merchantrequestid = "12345"
        #active_status =True
        book_time = datetime.datetime.now() 
        check_in_date = request.POST['ctime']
        stay_time = request.POST['stime']
        check_out_date = request.POST['otime']
        new_re=Room_application(booking_user=booking_user, booked_room=booked_room, booked_plot=booked_plot, 
         book_time=book_time, check_in_date=check_in_date,stay_time=stay_time,check_out_date=check_out_date )

        try:
            new_re.save()
            messages.success(request, "rental application send succesfully")
            return redirect("nyumba:rental_applications")
        except:
            messages.warning(request, "the applicaiton process failed, try again")
            return redirect("nyumba:rental_application_form")
    return render(request, 'nyumba/landlord/rental_application_form.html')
@login_required()
def landlord_reponse(request):
    if request.method == 'POST':
        r_id = request.POST['applicationId']
        app = Room_application.objects.get(id=r_id)
        app_room = app.booked_room
        choice = request.POST['choice']
        try:
            app.landlords_response = choice
            app.save()   
        except:
            messages.warning(request, "response failed, Try again!!")
            return redirect("nyumba:rental_applications")
        if choice == "1":
            app_room.room_status = True
            app_room.save()
            messages.success(request,"response send succesfully")
            return redirect("nyumba:rental_applications")
        else:
            messages.success(request, "send succesfully")
            return redirect("nyumba:rental_applications")
    return render(request, 'nyumba/landlord/rental_applications.html')
@login_required()
def add_new_tenant(request):
    if request.method == 'POST':
        t_id = request.POST['tenants']
        booking_user = myUser.objects.get(id=t_id)
        b_id = request.POST['unitid'] 
        booked_room = Room.objects.get(id=b_id) 
        booked_plot = booked_room.room_plot
        payment = request.POST['payment']
        landlord_response = 1
        merchantrequestid = "46736"
        book_time = datetime.datetime.now()
        check_in_date = request.POST['c_time']
        stay_time = request.POST['s_time']
        check_out_date = request.POST['o_time']
        newTenant = Room_application(booking_user=booking_user, booked_room=booked_room,booked_plot=booked_plot, landlords_response=landlord_response, merchantrequestid=merchantrequestid,
         payment_status=payment,book_time=book_time, check_in_date=check_in_date, stay_time=stay_time, check_out_date=check_out_date
         )
        try:
            newTenant.save()
            messages.success(request, "new Tenant added succesfully")
            return redirect("nyumba:tenants")
        except:
            messages.warning(request, "The process failed, try again!!")
            return redirect("nyumba:add_tenant")
    return render(request, "nyumba/landlord/add_tenant.html")

@login_required()        
def tenantinfo(request):
    if request.method == 'GET':
        tenantid = request.GET['tenant_id']
        current_tenant = myUser.objects.get(id=tenantid)
        #requestedmessage.message_status = True #change the unread status to read 
        #requestedmessage.save()
        ser_instance = serializers.serialize('json', [current_tenant,]) #serialize the django object to a json data
        return JsonResponse({ "instance":ser_instance}, safe=False, status=200)#using serialize method
    else:
        return JsonResponse("error", status=400)




# ................end.............
    

#Reports
@login_required()
def reports(request):
    return render(request, 'nyumba/landlord/reports.html')
#profile
@login_required()
def landlord_profile(request):
    return render(request, 'nyumba/landlord/profile.html')
@login_required()
def base(request):
    return render(request, 'nyumba/landlord/base.html')



####tenant views
def tenantbase(request):
    return render(request, 'nyumba/tenant/tenant_base.html')
@login_required()
def tenant_home(request): 
    user=request.user
    vunits=Room.objects.filter(room_status=False)[:4]
    count_units=Room.objects.filter(room_status=False).count()
    a_stores = Store.objects.filter(space_availability=True)[:3]
    count_store = Store.objects.filter(space_availability=True).count()
    count_landlords = myUser.objects.filter(is_landlord=True).count()
    count_tenants = myUser.objects.filter(is_tenant=True).count()
    count_p=Room_application.objects.filter(landlords_response=0,booking_user=user).count()
    count_s=Room_application.objects.filter(landlords_response=1,booking_user=user).count()
    count_d=Room_application.objects.filter(landlords_response=2,booking_user=user).count()
    return render(request, 'nyumba/tenant/tenant_home.html', {'vunits':vunits, 'a_stores':a_stores,'count_units':count_units,
    'count_store':count_store, 'count_landlords':count_landlords, 'count_tenants':count_tenants,'count_p':count_p,
    'count_s':count_s, 'count_d':count_d})
@login_required()
def explore_rentals(request):
    vunits=Room.objects.filter(room_status=False)
    return render(request, 'nyumba/tenant/explore_rentals.html', {'vunits':vunits})
def house_form(request, hid):
    house=Room.objects.get(id=hid)
    return render(request, 'nyumba/tenant/house_form.html', {'house':house} )
@login_required()
def renter_profile(request):
    return render(request, 'nyumba/tenant/renter_profile.html')
@login_required()
def rental_home(request):
    user=request.user
    houses = Room.objects.filter(room_tenant=user)
    return render(request, 'nyumba/tenant/rental_home.html', {'houses':houses})
@login_required()
def myapplications(request):
    user = request.user
    app = Room_application.objects.filter(booking_user=user).order_by('-book_time')
    return render(request, 'nyumba/tenant/myapplications.html', {'app':app})
@login_required()
def mymaintenance(request):
    user=request.user
    all_m=Maintenance.objects.filter(applying_user=user)
    return render(request, 'nyumba/tenant/mymaintenance.html',{'all_m':all_m})
@login_required()
def explore_stores(request):
    a_stores = Store.objects.filter(space_availability=True) 
    return render(request, 'nyumba/tenant/explore_stores.html', {'a_stores':a_stores})
@login_required
def store_app(request,storeId):
    currentStore=Store.objects.get(id=storeId)
    v_units=Store_unit.objects.filter(unit_store=currentStore, unit_status=True)
    return render(request, 'nyumba/tenant/store_app.html', {'currentStore':currentStore,'v_units':v_units})
@login_required
def mystoreapplications(request):
    user=request.user
    all_applications = Store_applications.objects.filter(applying_user=user)
    return render(request, 'nyumba/tenant/store_applications.html', {'all_applications':all_applications})

@login_required()
def my_messages(request):
    return render(request, 'nyumba/tenant/my_messages.html')
@login_required()
def tenant_profile(request):
    return render(request, 'nyumba/tenant/tenant_profile.html')
@login_required()
def menu(request):
    return render(request, 'nyumba/tenant/menu.html')
@login_required()
def tenant_mainForm(request):
    user=request.user
    user_units=Room.objects.filter(room_tenant=user)
    return render(request, 'nyumba/tenant/maintenanceApplicationform.html', {'user_units':user_units})

@login_required()
def tenant_transactions(request):
    total=0
    user=request.user
    all_t=Succesful_Room_payments.objects.filter(Paying_user=user)
    for j in all_t:
        total=total+j.Amount
    return render(request, 'nyumba/tenant/transactions.html', {'all_t':all_t, 'total':total})
#..............tenant action pages...........

@login_required
def print_receipt(request,rid ):
    user=request.user
    a_payments=Succesful_Room_payments.objects.filter(Paying_user=user)
    your_receipt=Room_application.objects.get(id=rid)
    template_path = 'nyumba/receipt.html'
    context = {'your_receipt': your_receipt,'a_payments':a_payments}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>') 
    return response

@login_required
def Tenant_bookingStore(request):
    if request.method == 'POST':
        user=request.user
        unit_id = request.POST['unitid']
        #storeid = request.POST['units']
        applied_unit = Store_unit.objects.get(id=unit_id)
        applied_store = applied_unit.unit_store 
        applying_user = user
        #payment_status = False
        #applied_store 
        goods=request.POST['goods']
        dgoods=request.POST['dgoods']
        starting_date = request.POST['s_date']
        ending_date = request.POST['e_date']
        application_time = datetime.datetime.now()
        new_app = Store_applications(applied_unit=applied_unit, applying_user=applying_user, applied_store=applied_store, 
        starting_date=starting_date, ending_date=ending_date, application_time=application_time, goods=dgoods)

        try:
            new_app.save()
            applied_unit.user_mzigo=user
            applied_unit.unit_status=False
            applied_unit.unit_mzigo=goods
            applied_unit.save()
            messages.success(request, "application send succesfully")
            return redirect("nyumba:mystoreapplications")
        except:
            messages.warning(request, "application failed, try again!!")
            return redirect("nyumba:explore_stores")
    return render(request, 'nyumba/tenant/explore_stores.html')
@login_required
def tenant_maintenance(request):
    if request.method == 'POST':
        user=request.user
        applying_user = user
        unit_id = request.POST['unitId']
        unit =  Room.objects.get(id=unit_id)
        unit_plot = unit.room_plot
        subject = request.POST['subject']
        problem = request.POST['problem']
        pro_image = request.FILES.get('pro_image', False)
        new_m =Maintenance(applying_user=applying_user, plot=unit_plot, room=unit, subject=subject, problem=problem, pr_image=pro_image)
        try:
            new_m.save()
            messages.success(request, "you request has been send succesfully")
            return redirect("nyumba:mymaintenance")
        except:
            messages.warning(request, "you request has failed!! please try again")
            return redirect("nyumba:tenantmainForm")
    return render(request, 'nyumba/landlord/maintenanceApplicationform.html') 


####global views
@login_required()
def logout_user(request):
	logout(request)
	return redirect('User_account:login')


#.....................messaging module.............
#inbox
@login_required
def inbox(request):
    users=myUser.objects.all()
    #new_chats = publichat.objects.filter(chat_status=False).count()
    #all_messages=message.objects.all().order_by('-date_sent')
    send_messages=Chat.objects.filter(sender=request.user).order_by('-date_sent')
    count_send=Chat.objects.filter(sender=request.user, message_status=False).count()
    count_texts=Chat.objects.filter(receiver=request.user.username, message_status=False).count()
    text_messages=Chat.objects.filter(receiver=request.user.username, hide_status=False).order_by('-date_sent')
    send_msg=Chat.objects.filter(sender=request.user, hide_status=False).order_by('-date_sent')
    #chats=publichat.objects.all().order_by('-time_sent')
    return render(request, 'nyumba/chats/inbox.html', {'text_messages':text_messages, 'users':users, 'count':count_texts,
         'send_msg':send_msg,})

#sending chat
@login_required 
@csrf_exempt
def send_chat(request):
    if request.method =='POST':
        sender=request.user
        subject=request.POST['subject']
        text=request.POST['message']
        recipient=request.POST['receiver']
        parent=request.POST.get('parent')
        today=datetime.datetime.now()
        new=Chat(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

        try:
            new.save()
            messages.success(request, 'Message Sent successfully')
            return redirect('nyumba:inbox')

        except:
            messages.error(request, 'Unable to Send Message')
            return redirect('nyumba:inbox')

    else:
       
        return  render(request, 'nyumba/chats/inbox.html')#{'texts':message_count})

#sending to landlord or tenant
# @login_required 
# @csrf_exempt
# def sending_toguide(request):
#     if request.method =='POST':
#         sender=request.user.username
#         subject=request.POST['subject']
#         text=request.POST['message']
#         recipient=request.POST['receiver']
#         parent=request.POST.get('parent')
#         today=datetime.datetime.now()
#         c=message(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

#         try:
#             c.save()
#             django_messages.success(request, 'Message Sent successfully')
#             return redirect('Tour:guide')

#         except:
#             django_messages.error(request, 'Unable to Send Message')
#             return redirect('Tour:guide')

#     else:
#         return  render(request, 'Tour/guides.html')

#sending a reply
@csrf_exempt
def send_reply(request):
    if request.method =='POST':
        sender=request.user
        subject=request.POST['subject']
        text=request.POST['message']
        #parent=request.POST.get(id=parentid)
        parentid=request.POST.get('parent')
        parent=Chat.objects.get(id=parentid)
        recipient=request.POST['receiver']
        today=datetime.datetime.now()
        reply=Chat(sender=sender,text=text,subject=subject,parent=parent,receiver=recipient,date_sent=today)

        try:
            reply.save()
            messages.success(request, 'repy send successfully ')
            return redirect('Tour:load')

        except:
            messages.error(request, 'Unable to Send Message')
            return redirect('Tour:load')

    else:
        return  render(request, 'nyumba/chats/inbox.html')#,{'texts':message_count})

#displaying a single message after a user clicks it
@login_required 
def single_chat(request):
    if request.method == 'GET':
        messageid = request.GET['message_id']
        requestedmessage = Chat.objects.get(id=messageid)
        requestedmessage.message_status = True #change the unread status to read 
        requestedmessage.save()
        ser_instance = serializers.serialize('json', [requestedmessage,]) #serialize the django object to a json data
        return JsonResponse({ "instance":ser_instance}, safe=False, status=200)#using serialize method
    else:
        return JsonResponse("error", status=400)
#deleting a message
@login_required
def delete_chat(request):
    if request.method == 'POST':
        msg_id = request.POST['del_chat']
        msg = Chat.objects.get(id=msg_id)
        msg.delete()
        messages.success(request,"message deleted successfully")
        return redirect('nyumba:inbox')
    else:
        messages.success(request,"the chat was not deleted")
        return redirect('nyumba:inbox')

#hiding a message
@login_required
def Hide_msg(request):
    if request.method == 'POST':
        msg_id = request.POST['hide_chat']
        msg = Chat.objects.get(id=msg_id)
        msg.hide_status = True
        msg.save()
        messages.success(request,"message hidden successfully")
        return redirect('nyumba:inbox')
    else:
        return redirect('nyumba:inbox')
    