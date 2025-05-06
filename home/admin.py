
from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import PendingAd, ConfirmedAd, PropertyFeature,PendingAdImage, ConfirmedAdImage
from django.core.files.base import ContentFile # Needed for image handling if paths differ
import os
from django.conf import settings
from django.contrib import admin
from .models import HousePriceIndex, LandPriceIndex

# Register the models
class ConfirmedAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'offer_type', 'created_at')
    list_filter = ('city', 'property_type', 'offer_type', 'created_at')
    search_fields = ('title', 'city', 'description', 'street')

admin.site.register(ConfirmedAd,ConfirmedAdAdmin)
admin.site.register(PropertyFeature)

#Custom Admin for PendingAd
class PendingAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'offer_type', 'created_at' )
    list_filter = ('city', 'property_type', 'offer_type', 'created_at')
    search_fields = ('title', 'city', 'description', 'street')
    actions = ['approve_and_move_ads']

    @admin.action(description='Approve selected ads and move to Confirmed Ads')
    def approve_and_move_ads(self, request, queryset):
        """
        Approves selected PendingAd objects, creates ConfirmedAd objects,
        and transfers associated images.
        """
        successful_count = 0
        errors = []

        for pending_ad in queryset:
            try:

                address = f"{pending_ad.street}, {pending_ad.city}" if pending_ad.street else pending_ad.city
                details_text = pending_ad.description or ''
                if pending_ad.latitude and pending_ad.longitude:
                    details_text += f"\nCoordinates: ({pending_ad.latitude}, {pending_ad.longitude})"
                if pending_ad.price_type:
                     details_text += f"\nPrice Type: {pending_ad.price_type}"
                if pending_ad.user_type:
                     details_text += f"\nSubmitted By User Type: {pending_ad.user_type}"

                confirmed_ad = ConfirmedAd(
                    title=pending_ad.title or "Untitled Ad",
                    description=pending_ad.description or "No description provided.",
                    address=address,
                    city=pending_ad.city,
                    street=pending_ad.street,
                    latitude=pending_ad.latitude,
                    longitude=pending_ad.longitude,
                    price=pending_ad.price or 0.00,
                    price_type=pending_ad.price_type,
                    details=details_text.strip(),
                    property_type=pending_ad.property_type,
                    offer_type=pending_ad.offer_type,
                    bedrooms=pending_ad.bedrooms or 0,
                    bathrooms=pending_ad.bathrooms or 0,
                    floor_area=pending_ad.floor_area or 0.0,
                    floors=pending_ad.floors or 0,
                    age_of_building=pending_ad.age or 0,
                    status=pending_ad.status or 'Unknown',
                    parking=pending_ad.parking,
                    furnishing_status=pending_ad.furnishing or 'Unfurnished',
                    land_area=0.0,
                    seller_name=pending_ad.registered_name or "Pending Review",
                    seller_tel=pending_ad.registered_contact or "Pending Review",
                    seller_email=pending_ad.registered_email or "pending@review.com",

                )
                confirmed_ad.save()

                # --- Transfer Images  ---
                pending_ad_images = PendingAdImage.objects.filter(pending_ad=pending_ad)
                for pending_image in pending_ad_images:
                    try:
                        # Read the content of the pending image file
                        image_content = pending_image.image.read()
                        # Construct a filename for the new confirmed ad image
                        file_name = os.path.basename(pending_image.image.name)
                        # Create a ContentFile
                        confirmed_image_file = ContentFile(image_content, name=file_name)
                        # Create the ConfirmedAdImage object
                        ConfirmedAdImage.objects.create(
                            confirmed_ad=confirmed_ad,
                            image=confirmed_image_file
                        )
                    except Exception as img_err:
                        errors.append(f"Error transferring image for Pending Ad {pending_ad.id}: {img_err}")
                    finally:

                        pending_image.image.seek(0)

                # --- Handle ManyToMany Features---
                if pending_ad.features:
                    feature_names = [name.strip() for name in pending_ad.features.split(',') if name.strip()]
                    for feature_name in feature_names:
                        feature, created = PropertyFeature.objects.get_or_create(name=feature_name)
                        confirmed_ad.property_features.add(feature)

                # --- Cleanup ---
                pending_ad.delete()
                successful_count += 1

            except Exception as e:
                errors.append(f"Error processing Pending Ad ID {pending_ad.id} ({pending_ad.title}): {e}")
                # import traceback
                # print(traceback.format_exc())

        # --- Report Results to Admin  ---
        if successful_count > 0:
            self.message_user(request, ngettext(
                '%d pending ad was successfully approved and moved.',
                '%d pending ads were successfully approved and moved.',
                successful_count,
            ) % successful_count, messages.SUCCESS)

        if errors:
            self.message_user(request, "Errors occurred during processing:", messages.ERROR)
            for error in errors:
                self.message_user(request, error, messages.WARNING)

# Register the PendingAd model with the custom admin class
admin.site.register(PendingAd, PendingAdAdmin)

admin.site.register(HousePriceIndex)
admin.site.register(LandPriceIndex)