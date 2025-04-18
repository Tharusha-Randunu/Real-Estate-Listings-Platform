from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    phone_number = forms.CharField(max_length=20, required=False, help_text='Optional')
    profile_picture = forms.ImageField(required=False, help_text='Optional: Upload your profile picture')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "profile_picture")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        if commit:
            user.save()
            # Save phone number to UserProfile
            phone_number = self.cleaned_data.get("phone_number")
            # Create UserProfile and save the profile picture if it's provided
            profile = UserProfile.objects.create(user=user, phone_number=phone_number)
            if self.cleaned_data.get("profile_picture"):
                profile.profile_picture = self.cleaned_data.get("profile_picture")
                profile.save()
        return user

class LoginForm(AuthenticationForm):
    pass
