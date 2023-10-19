from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(UserChangeForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'User Name',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

        widgets = {
            'email': forms.TextInput(
                attrs={'class': "form-control", 'type': "email", 'aria-label': "Email", 'aria-describedby': "basic-addon2", "font-size": "10px"}),
            'first_name': forms.TextInput(
                attrs={'class': "form-control", 'type': "text", 'aria-label': "First Name", 'aria-describedby': "basic-addon2", "font-size": "10px"}),
            'last_name': forms.TextInput(
                attrs={'class': "form-control", 'type': "text", 'aria-label': "Last Name", 'aria-describedby': "basic-addon2", "font-size": "10px"}),
            'username': forms.TextInput(
                attrs={'class': "form-control", 'type': "text", 'aria-label': "User Name", 'aria-describedby': "basic-addon2", "font-size": "10px"}),
        }
