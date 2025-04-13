

# Register your models here.
from django.contrib import admin
from .models import PendingAd, ConfirmedAd, PropertyFeature

admin.site.register(ConfirmedAd)
admin.site.register(PropertyFeature)
admin.site.register(PendingAd)