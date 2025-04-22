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
        fields = ("username", "email", "first_name", "last_name", "phone_number", "profile_picture", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()
            phone_number = self.cleaned_data.get("phone_number")
            profile_picture = self.cleaned_data.get("profile_picture")
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                profile_picture=profile_picture
            )
        return user

class LoginForm(AuthenticationForm):
    pass

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture']

    phone_number = forms.CharField(max_length=20, required=False, help_text="Optional")
    profile_picture = forms.ImageField(required=False, help_text="Optional: Upload a new profile picture")

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
        return user_profile