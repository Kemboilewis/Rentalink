from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import myUserCreationForm, MyUserChangeForm
from .models import myUser

class CustomUserAdmin(UserAdmin):
    add_form = myUserCreationForm
    form = MyUserChangeForm
    model = myUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_tenant', 'is_landlord','id_number',
    'Phone_number','profile_image','is_staff', 'is_active','id_copy']
    #list_display = ['email', 'username',]
    fieldsets = UserAdmin .fieldsets + (
        (None, {'fields':('is_tenant','is_landlord','id_number','Phone_number','profile_image','id_copy')}),
    )#this allow the admin to change this pages

admin.site.register(myUser, CustomUserAdmin)