from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import *

def index(request):
    return render(request, 'user_account/index.html')

#registration and login templates
def register_template(request):
    return render(request, 'user_account/register_template.html')

def login_template(request):
    return render(request, 'user_account/login_template.html')

#login, logout and registration views
def loginuser(request):
	if request.method =='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		#check if the user has correct credentials
		if user is not None:
			login(request,user)
			if user.is_landlord == True:
				return redirect('nyumba:landlord_home')
			else:
				return redirect('nyumba:tenant_home')
		else:
			messages.warning(request, 'INVALID CREDENTIALS!!!')
			return render(request, 'user_account/index.html')

@login_required()
def logout_user(request): 
	logout(request)
	return redirect('user_account:index')

def register(request):
	if request.method == 'POST': 
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		id_number = request.POST['id_number']
		contact = request.POST['contact']
		id_copy = request.POST.get('id_copy', False)
		profile_image = request.POST.get('profile_image', False)
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		landlord = request.POST['landlord']
		tenant = request.POST['tenant']
		
		#create user
		
		try:
			newuser = myUser.objects.create_user(username=username,password=password,first_name=first_name, last_name=last_name, id_number=id_number, 
		Phone_number=contact,profile_image=profile_image,email=email,is_tenant=tenant, is_landlord=landlord)
			messages.success(request, 'account created succesfully , login')
			#newuser.save()
			return redirect('user_account:index')
			
		except:
			messages.error(request, 'unable to create your account')
			return redirect('user_account:index')
	else:
		return redirect('user_account:tenant_register_template')

