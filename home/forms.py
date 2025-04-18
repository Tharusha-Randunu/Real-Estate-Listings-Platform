from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Added AuthenticationForm import
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class LoginForm(AuthenticationForm):
    pass