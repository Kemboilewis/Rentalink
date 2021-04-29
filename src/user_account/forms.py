from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import myUser


class myUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = myUser
        #fields = ('username', 'email')
        fields = ('username', 'first_name', 'last_name', 'email', 'is_tenant', 'is_landlord','id_number',
    'Phone_number','profile_image','is_staff', 'is_active', 'id_copy')

class MyUserChangeForm(UserChangeForm):

    class meta(UserChangeForm):
        model = myUser
        #fields = ('username', 'email')
        fields = ('username', 'first_name', 'last_name', 'email', 'is_tenant', 'is_landlord','id_number',
    'Phone_number','profile_image','is_staff', 'is_active', 'id_copy')