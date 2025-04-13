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
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    floor_area = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)