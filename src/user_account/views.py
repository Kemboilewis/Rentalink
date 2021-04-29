from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import *

def index(request):
    return render(request, 'User_account/index.html')

#registration and login templates
def register_template(request):
    return render(request, 'User_account/register_template.html')

def login_template(request):
    return render(request, 'User_account/login_template.html')

#login, logout and registration views
def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if user.is_landlord == True:
                return redirect('nyumba:landlord_home')
            else:
                return redirect('nyumba:tenant_home')
        #check if the user has correct credentials
            django_messages.warning(request, 'INVALID CREDENTIALS!!!')
            return render(request, 'User_account/login.html')

@login_required()
def logout_user(request):
	logout(request)
	return redirect('User_account:login')

def register_tenant(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		id_number = request.POST['id_number']
		contact = request.POST['contact']
		id_copy = request.POST.get('id_copy', False)
		profile_image = request.POST.get('profile_image', False)
		email = request.POST['email']
		username = request.POST['user_name']
		password = request.POST['password']
		
		#create user
		user = myUser(username=username,password=password,first_name=first_name, last_name=last_name, id_number=id_number, 
		Phone_number=contact,profile_image=profile_image,email=email,is_tenant=True)
		try:
			user.save()
			return redirect('User_account:login')
			
		except:
			django_messages.error(request, 'unable to create your account')
			return redirect('User_account:tenant_register_template')
	else:
		return redirect('User_account:tenant_register_template')


def register_landlord(request):
	if request.method == 'POST':

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		id_number = request.POST['id_number']
		contact = request.POST['contact']
		id_copy = request.POST.get('id_copy', False)
		profile_image = request.POST.get('profile_image', False)
		email = request.POST['email']
		username = request.POST['user_name']
		password = request.POST['password']
		
		#crete user
		user = myUser(username=username,password=password,first_name=first_name, last_name=last_name, 
		id_number=id_number, Phone_number=contact,profile_image=profile_image,email=email,is_landlord=True)
		try:
			user.save()
			login(request,user)
			return redirect('User_account:login')
			
		except:
			django_messages.error(request, 'unable to create your account')
			return redirect('User_account:landlord_register_template')
	else:
		return redirect('User_account:landlord_register_template')
