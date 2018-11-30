from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# the sign up form. it uses the default UserRegisterForm and adds to attributes
# to it: name (which is not realy required) and email
class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','password1','password2','name','email']


# this to classes are for updating the user profile page when the user changes
# his username, email or profile picture. other fiels like name and password can
# be added to
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
