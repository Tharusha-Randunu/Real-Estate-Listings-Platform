from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import ConfirmedAd
from django.contrib.auth.forms import PasswordChangeForm



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = UserProfile.objects.create(user=user,
                                                phone_number=self.cleaned_data['phone_number'],
                                                profile_picture=self.cleaned_data['profile_picture'])
            return user, profile  # Return both user and profile
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


class PasswordChangeFormCustom(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Old Password")
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="New Password")
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label="Confirm New Password")

class ConfirmedAdForm(forms.ModelForm):
    class Meta:
        model = ConfirmedAd
        fields = ['title', 'description', 'address', 'city', 'street', 'latitude', 'longitude', 'price', 'price_type', 'property_type', 'offer_type', 'bedrooms', 'bathrooms', 'land_area', 'floor_area', 'floors', 'age_of_building', 'status', 'parking', 'property_features', 'furnishing_status', 'seller_name', 'seller_tel', 'seller_email',  'link',  'user']