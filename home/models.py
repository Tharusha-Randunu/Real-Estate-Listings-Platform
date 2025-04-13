from django.db import models

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

    PROPERTY_FEATURES = [
        ('AC', 'Air Conditioning'),
        ('Beachfront', 'Beachfront'),
        ('Indoor Garden', 'Indoor Garden'),
        ('Garage', 'Garage'),
        ('Swimming Pool', 'Swimming Pool'),
        ('Hot Water', 'Hot Water'),
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
    property_features = models.ManyToManyField("PropertyFeature", blank=True)
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_STATUS)
    seller_name = models.CharField(max_length=255)
    seller_tel = models.CharField(max_length=15)
    seller_email = models.EmailField()
    images = models.ImageField(upload_to='property_images/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)

class PropertyFeature(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class PendingAd(models.Model):
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Land', 'Land'),
        ('Commercial', 'Commercial'),
        ('Bungalow', 'Bungalow'),
        ('Villa', 'Villa'),
        ('Annexe', 'Annexe'),
        ('Rooms', 'Rooms'),
        ('Studio', 'Studio'),
    ]

    OFFER_TYPES = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
    ]

    FURNISHING_STATUS = [
        ('Fully Furnished', 'Fully Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Unfurnished', 'Unfurnished'),
    ]

    STATUS_CHOICES = [
        ('Available Now', 'Available Now'),
        ('Available Soon', 'Available Soon'),
        ('Offer Received', 'Offer Received'),
        ('Price Reduced', 'Price Reduced'),
    ]

    # Section: I Am
    posted_by = models.CharField(max_length=50)  # Owner / Agent / Developer / Business

    # Offer Type
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    # Property Type
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)

    # Location Section
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Basic Details Section
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    floor_area = models.FloatField()

    # Price Details Section
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_type = models.CharField(max_length=20, default='Per Month')  # or Per Week/Per Day etc.

    # Property Specifics Section
    floors = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    age_of_building = models.IntegerField(blank=True, null=True)
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_STATUS, blank=True, null=True)
    parking = models.BooleanField(default=False)

    # Ad Details Section
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Property Features (checkbox group)
    property_features = models.ManyToManyField(PropertyFeature, blank=True)

    # Contact Details Section (optional, if you're collecting here)
    seller_name = models.CharField(max_length=255, blank=True, null=True)
    seller_tel = models.CharField(max_length=15, blank=True, null=True)
    seller_email = models.EmailField(blank=True, null=True)

    # Image Uploads (optional at this stage)
    images = models.ImageField(upload_to='pending_property_images/', null=True, blank=True)

    # Link field (if the ad is externally linked later)
    link = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # helpful for admin sorting

    def __str__(self):
        return f"{self.title} ({self.city}) - {self.offer_type}"
