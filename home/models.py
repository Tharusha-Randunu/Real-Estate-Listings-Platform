from django.db import models
from django.contrib.auth.models import User

class PropertyFeature(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

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

    name = models.CharField(max_length=255)
    address = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.TextField()
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
    images = models.ImageField(upload_to='property_images/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)

class PendingAd(models.Model):
    # --- Fields from rent_register.html ---
    registered_name = models.CharField(max_length=255, default='') # Added default
    registered_email = models.EmailField(default='')             # Added default
    registered_contact = models.CharField(max_length=20, default='') # Added default
    registered_district = models.CharField(max_length=100, default='') # Added default


    # Fields from rent_property.html
    user_type = models.CharField(max_length=50, blank=True, null=True) # Owner, Agent, etc.
    offer_type = models.CharField(max_length=10, default='Rent') # Rent/Sale
    property_type = models.CharField(max_length=50, blank=True, null=True) # House, Apartment, etc.
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Fields from rent_property_details.html
    bedrooms = models.PositiveIntegerField(null=True, blank=True) # Make nullable temporarily if not always required
    bathrooms = models.PositiveIntegerField(null=True, blank=True)# Make nullable temporarily if not always required
    floor_area = models.PositiveIntegerField(null=True, blank=True) # Make nullable temporarily if not always required
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # Make nullable temporarily
    price_type = models.CharField(max_length=50, blank=True, null=True)
    floors = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True) # Available Now, etc.
    age = models.PositiveIntegerField(blank=True, null=True) # Age of Property
    furnishing = models.CharField(max_length=50, blank=True, null=True) # Fully Furnished, etc.
    parking = models.BooleanField(default=False) # Parking Available
    title = models.CharField(max_length=255, blank=True, null=True) # Make nullable temporarily
    description = models.TextField(blank=True, null=True) # Make nullable temporarily
    features = models.TextField(blank=True, null=True) # Store selected features (e.g., comma-separated)

    # Fields from upload_confirm.html
    property_image = models.ImageField(upload_to='pending_property_images/', null=True, blank=True) # Use a different path?
    confirmed_ownership = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending Ad: {self.title} in {self.city}"

    class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
        phone_number = models.CharField(max_length=20, blank=True)

        # Add other profile fields as needed

        def __str__(self):
            return self.user.username
