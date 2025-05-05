from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


# Represents a specific feature that a property can have (e.g., garden, pool)
class PropertyFeature(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Stores confirmed property listings that are publicly visible
class ConfirmedAd(models.Model):
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Land', 'Land'),
        ('Commercial', 'Commercial'),
    ]

    OFFER_TYPES = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
    ]

    FURNISHING_STATUS = [
        ('Furnished', 'Furnished'),
        ('Semi-Furnished', 'Semi-Furnished'),
        ('Unfurnished', 'Unfurnished'),
    ]

    # Basic property info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    details = models.TextField(blank=True,null=True)
    address = models.TextField()
    city = models.CharField(max_length=100,blank=True,null=True)
    street = models.CharField(max_length=100,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_type = models.CharField(max_length=50,blank=True,null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    land_area = models.FloatField()
    floor_area = models.FloatField()
    floors = models.IntegerField()
    age_of_building = models.IntegerField()
    status = models.CharField(max_length=50)
    parking = models.BooleanField(default=False)
    property_features = models.ManyToManyField(PropertyFeature, blank=True)
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_STATUS)
    seller_name = models.CharField(max_length=255)
    seller_tel = models.CharField(max_length=15)
    seller_email = models.EmailField()
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title or f"Confirmed Ad {self.id}"

# Stores images related to a confirmed ad listing
class ConfirmedAdImage(models.Model):
    """Stores multiple images related to a ConfirmedAd."""
    confirmed_ad = models.ForeignKey(ConfirmedAd, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='confirmed_ad_images/') # Specific path for confirmed ad images
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        try:
            return f"Image for {self.confirmed_ad.title} ({self.id})"
        except ConfirmedAd.DoesNotExist:
             return f"Image for deleted ad ({self.id})"


# Stores property listings submitted by users that are pending admin approval
class PendingAd(models.Model):

    registered_name = models.CharField(max_length=255, default='')
    registered_email = models.EmailField(default='')
    registered_contact = models.CharField(max_length=20, default='')
    registered_district = models.CharField(max_length=100, default='')


    # Fields from rent_property.html
    user_type = models.CharField(max_length=50, blank=True, null=True)
    offer_type = models.CharField(max_length=10, default='Rent')
    property_type = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Fields from rent_property_details.html
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    floor_area = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=50, blank=True, null=True)
    floors = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    furnishing = models.CharField(max_length=50, blank=True, null=True)
    parking = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)

    # Fields from upload_confirm.html
    confirmed_ownership = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending Ad: {self.title} in {self.city}"


# Stores images related to a pending ad listing
class PendingAdImage(models.Model):
    """Stores multiple images related to a PendingAd."""
    pending_ad = models.ForeignKey(PendingAd, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pending_ad_images/') # Specific path for pending ad images
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        try:
            return f"Image for Pending Ad: {self.pending_ad.title} ({self.id})"
        except PendingAd.DoesNotExist:
             return f"Image for deleted pending ad ({self.id})"


# Extended profile model linked to Django's built-in User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Stores house price index data per region and quarter
class HousePriceIndex(models.Model):
    region = models.CharField(max_length=100)
    quarter = models.CharField(max_length=10)  # e.g., '2022 Q1'
    price_index = models.FloatField()

    def __str__(self):
        return f"{self.region} - {self.quarter}"


# Stores land price index data per city and quarter
class LandPriceIndex(models.Model):
    city = models.CharField(max_length=100)
    quarter = models.CharField(max_length=10)
    price_index = models.FloatField()

    def __str__(self):
        return f"{self.city} - {self.quarter}"