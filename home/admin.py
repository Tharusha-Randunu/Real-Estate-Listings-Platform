
from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import PendingAd, ConfirmedAd, PropertyFeature
from django.core.files.base import ContentFile # Needed for image handling if paths differ
import os
from django.conf import settings

# Register the simple models first

class ConfirmedAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'offer_type', 'created_at')
    list_filter = ('city', 'property_type', 'offer_type', 'created_at')
    search_fields = ('title', 'city', 'description', 'street')

admin.site.register(ConfirmedAd,ConfirmedAdAdmin)
admin.site.register(PropertyFeature)

# --- Custom Admin for PendingAd ---
class PendingAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'offer_type', 'created_at' )
    list_filter = ('city', 'property_type', 'offer_type', 'created_at')
    search_fields = ('title', 'city', 'description', 'street')
    actions = ['approve_and_move_ads'] # Add the custom action here

    @admin.action(description='Approve selected ads and move to Confirmed Ads')
    def approve_and_move_ads(self, request, queryset):
        """
        Approves selected PendingAd objects, creates ConfirmedAd objects,
        and deletes the original PendingAd objects.
        """
        successful_count = 0
        errors = []

        for pending_ad in queryset:
            try:
                # --- Field Mapping ---
                # Combine city and street for address
                address = f"{pending_ad.street}, {pending_ad.city}" if pending_ad.street else pending_ad.city

                # Prepare details field (can include extra info)
                details_text = pending_ad.description or ''
                if pending_ad.latitude and pending_ad.longitude:
                    details_text += f"\nCoordinates: ({pending_ad.latitude}, {pending_ad.longitude})"
                if pending_ad.price_type:
                     details_text += f"\nPrice Type: {pending_ad.price_type}"
                if pending_ad.user_type:
                     details_text += f"\nSubmitted By User Type: {pending_ad.user_type}"


                # Create the ConfirmedAd instance
                confirmed_ad = ConfirmedAd(
                    title=pending_ad.title or "Untitled Ad",  # Use title for name
                    description=pending_ad.description or "No description provided.",
                    address=address,
                    city=pending_ad.city,
                    street=pending_ad.street,
                    latitude=pending_ad.latitude,
                    longitude=pending_ad.longitude,
                    price=pending_ad.price or 0.00,  # Provide default if nullable
                    price_type=pending_ad.price_type,
                    details=details_text.strip(),
                    property_type=pending_ad.property_type,
                    offer_type=pending_ad.offer_type,
                    bedrooms=pending_ad.bedrooms or 0,  # Provide default if nullable
                    bathrooms=pending_ad.bathrooms or 0,  # Provide default if nullable
                    floor_area=pending_ad.floor_area or 0.0,  # Provide default if nullable
                    floors=pending_ad.floors or 0,  # Provide default if nullable
                    age_of_building=pending_ad.age or 0,  # Use age field, provide default
                    status=pending_ad.status or 'Unknown',  # Provide default
                    parking=pending_ad.parking,
                    furnishing_status=pending_ad.furnishing or 'Unfurnished',  # Map furnishing, provide default
                    # --- Fields requiring manual input or defaults ---
                    land_area=0.0,  # Default - Needs manual update later if important
                    seller_name=pending_ad.registered_name or "Pending Review",
                    # Use registered name as initial seller name
                    seller_tel=pending_ad.registered_contact or "Pending Review",
                    # Use registered contact as initial seller tel
                    seller_email=pending_ad.registered_email or "pending@review.com",
                    # Use registered email as initial seller email
                    # link=None # Default is blank/null
                )

                # --- Handle Image ---
                if pending_ad.property_image:
                    # Just assign the file object. Django handles moving/copying
                    # based on storage backend settings if needed.
                    # Ensure MEDIA_ROOT and upload_to paths are correctly configured.
                    confirmed_ad.images.save(
                        os.path.basename(pending_ad.property_image.name),
                        pending_ad.property_image, # Pass the FieldFile directly
                        save=False # Don't save the ConfirmedAd model yet
                    )
                    # Note: If storages differ significantly, you might need to read
                    # the content and save it as a new file:
                    # image_content = ContentFile(pending_ad.property_image.read())
                    # confirmed_ad.images.save(os.path.basename(pending_ad.property_image.name), image_content, save=False)


                # Save the ConfirmedAd first to get an ID for ManyToMany relations
                confirmed_ad.save()

                # --- Handle ManyToMany Features ---
                if pending_ad.features:
                    feature_names = [name.strip() for name in pending_ad.features.split(',') if name.strip()]
                    for feature_name in feature_names:
                        feature, created = PropertyFeature.objects.get_or_create(name=feature_name)
                        confirmed_ad.property_features.add(feature)

                # --- Cleanup ---
                # Delete the original PendingAd
                # Important: Close the image file *before* deleting the pending_ad object
                # if you manually read its content earlier. Assigning the FieldFile is safer.
                if pending_ad.property_image:
                    pending_ad.property_image.close() # Good practice

                pending_ad.delete()
                successful_count += 1

            except Exception as e:
                # Log the error and notify the admin
                errors.append(f"Error processing Pending Ad ID {pending_ad.id} ({pending_ad.title}): {e}")
                # Consider logging the full traceback here for debugging:
                # import traceback
                # print(traceback.format_exc())


        # --- Report Results to Admin ---
        if successful_count > 0:
            self.message_user(request, ngettext(
                '%d pending ad was successfully approved and moved.',
                '%d pending ads were successfully approved and moved.',
                successful_count,
            ) % successful_count, messages.SUCCESS)

        if errors:
            self.message_user(request, "Errors occurred during processing:", messages.ERROR)
            for error in errors:
                self.message_user(request, error, messages.WARNING) # Show individual errors


# Register the PendingAd model with the custom admin class
admin.site.register(PendingAd, PendingAdAdmin)