from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
import mimetypes
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ConfirmedAd, PropertyFeature, PendingAd
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation

# --- Helper function to safely convert to float ---
def safe_float(value, default=None):
    if value is None or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# --- Helper function to safely convert to int ---
def safe_int(value, default=None):
    if value is None or value == '':
        return default
    try:
        # Handle cases like '6+' -> 6
        if isinstance(value, str) and value.endswith('+'):
             value = value[:-1]
        return int(value)
    except (ValueError, TypeError):
        return default

# --- Helper function to safely convert to Decimal ---
def safe_decimal(value, default=None):
    if value is None or value == '':
        return default
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError): # InvalidOperation used here too!
        return default

def home(request):
    latest_ads = ConfirmedAd.objects.order_by('-id')[:4]
    return render(request, 'home/home.html', {'latest_ads': latest_ads})

def list_property(request):
    return render(request, 'home/list_property.html')

def rent_property(request):
    return render(request, 'home/rent_property.html')

def find_a_home(request):
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    property_type = request.GET.get('property_type', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    features = request.GET.getlist('features', [])
    offer_type = request.GET.get('offer_type', '')

    # Convert bedrooms to an integer if it's provided
    if bedrooms:
        bedrooms = int(bedrooms)

    if bathrooms:
        bathrooms = int(bathrooms)

    # Start with all ads
    ads = ConfirmedAd.objects.all()

    if query:
        ads = ads.filter(Q(name__icontains=query) | Q(details__icontains=query))
    if city:
        ads = ads.filter(address__icontains=city)
    if property_type:
        ads = ads.filter(property_type=property_type)
    if bedrooms:
        ads = ads.filter(bedrooms=bedrooms)
    if bathrooms:
        ads = ads.filter(bathrooms=bathrooms)
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)
    if offer_type:
        ads = ads.filter(offer_type=offer_type)

    # Apply filtering for features (many-to-many relationship)
    if features:
        ads = ads.filter(property_features__in=features)

    # Get the available features for the filter dropdown
    available_features = PropertyFeature.objects.all()
    # Pass a range of numbers for the bedroom selection
    bedroom_range = range(1, 11)  # Numbers 1 to 10
    bathroom_range = range(1, 11)  # Numbers 1 to 10

    return render(request, 'home/find_a_home.html', {
        'ads': ads,
        'query': query,
        'city': city,
        'property_type': property_type,
        'bedrooms': bedrooms,
        'bedroom_range': bedroom_range,
        'bathrooms': bathrooms,
        'bathroom_range': bathroom_range,
        'min_price': min_price,
        'max_price': max_price,
        'available_features': available_features,
        'selected_features': features,
        'offer_type': offer_type,

    })

def property_detail(request, ad_id):
    ad = get_object_or_404(ConfirmedAd, id=ad_id)
    return render(request, 'home/property_detail.html', {'ad': ad})

def serve_image(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        with open(media_path, 'rb') as img_file:
            mime_type, _ = mimetypes.guess_type(media_path)
            return HttpResponse(img_file.read(), content_type=mime_type or 'application/octet-stream')
    except FileNotFoundError:
        return HttpResponse(status=404)

def seller_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        district = request.POST.get('district')
        print(f"Name: {full_name}, Email: {email}, Contact: {contact}, District: {district}")
        return render(request, 'home/list_property.html')
    return render(request, 'home/seller_register.html')

def rent_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        district = request.POST.get('district')
        print(f"Name: {full_name}, Email: {email}, Contact: {contact}, District: {district}")
        return render(request, 'home/rent_property.html')
    return render(request, 'home/rent_register.html')

def market_insights_page(request):
    return render(request, 'home/market_insights.html')

def agent(request):
    return render(request, 'home/agent.html')

def list_property_details(request):
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]
    return render(request, 'home/list_property_details.html', {'features': features})

# --- Step 1: Collect Basic Info ---
def rent_property(request):
    if request.method == 'POST':
        # Extract data from POST request
        basic_info = {
            'user_type': request.POST.get('user_type'),
            'offer_type': request.POST.get('offer_type', 'Rent'), # Default to Rent
            'property_type': request.POST.get('property_type'),
            'city': request.POST.get('city'),
            'street': request.POST.get('street'),
            'latitude': request.POST.get('latitude'),
            'longitude': request.POST.get('longitude'),
        }
        # Store in session
        request.session['rent_basic_info'] = basic_info
        print("Saved basic info to session:", basic_info) # Debugging
        # Redirect to the next step
        return redirect('rent_property_details') # Redirect using URL name

    # If GET request, just show the form
    return render(request, 'home/rent_property.html')

# --- Step 2: Collect Property Details ---
def rent_property_details(request):
    # Define features here or get from DB if dynamic
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]

    if request.method == 'POST':
        # Extract data from POST request
        details_info = {
            'bedrooms': request.POST.get('bedrooms'),
            'bathrooms': request.POST.get('bathrooms'),
            'floor_area': request.POST.get('floor_area'),
            'price': request.POST.get('price'),
            'price_type': request.POST.get('price_type'),
            'floors': request.POST.get('floors'),
            'status': request.POST.get('status'),
            'age': request.POST.get('age'),
            'furnishing': request.POST.get('furnishing'),
            'parking': request.POST.get('parking') == 'true', # Checkbox value
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'features_list': request.POST.get('features_list'), # Comma-separated string
        }
        # Store in session
        request.session['rent_details_info'] = details_info
        print("Saved details info to session:", details_info) # Debugging
        # Redirect to the final confirmation step
        return redirect('upload_confirm') # Redirect using URL name

    # If GET request, show the form
    # Check if basic info exists from step 1, otherwise redirect back
    if 'rent_basic_info' not in request.session:
         print("Basic info missing, redirecting to rent_property") # Debugging
         # Optionally add a message: from django.contrib import messages; messages.error(request, 'Please start from step 1.')
         return redirect('rent_property')

    return render(request, 'home/rent_property_details.html', {'features': features})


# --- Step 3: Upload Image and Confirm ---
def upload_confirm(request):
    if request.method == 'POST':
        confirm = request.POST.get('confirm') == 'true' # Checkbox value
        image = request.FILES.get('property_image')

        # Retrieve data from session
        basic_info = request.session.get('rent_basic_info')
        details_info = request.session.get('rent_details_info')

        # --- Validation ---
        error_msg = None
        if not basic_info or not details_info:
            error_msg = 'Session expired or data missing. Please restart the ad submission.'
        elif not confirm:
            error_msg = 'You must confirm ownership/authorization.'
        elif not image:
             error_msg = 'Please upload a property image.'

        if error_msg:
             print("Error during submission:", error_msg) # Debugging
             # Don't clear session here so user might retry if applicable
             return render(request, 'home/upload_confirm.html', {'error': error_msg})
        # --- End Validation ---


        try:
            # --- Create PendingAd instance ---
            ad = PendingAd(
                # From basic_info
                user_type=basic_info.get('user_type'),
                offer_type=basic_info.get('offer_type', 'Rent'),
                property_type=basic_info.get('property_type'),
                city=basic_info.get('city'),
                street=basic_info.get('street'),
                latitude=safe_float(basic_info.get('latitude')),
                longitude=safe_float(basic_info.get('longitude')),

                # From details_info
                bedrooms=safe_int(details_info.get('bedrooms')),
                bathrooms=safe_int(details_info.get('bathrooms')),
                floor_area=safe_int(details_info.get('floor_area')),
                price=safe_decimal(details_info.get('price')),
                price_type=details_info.get('price_type'),
                floors=safe_int(details_info.get('floors')),
                status=details_info.get('status'),
                age=safe_int(details_info.get('age')),
                furnishing=details_info.get('furnishing'),
                parking=details_info.get('parking', False),
                title=details_info.get('title'),
                description=details_info.get('description'),
                features=details_info.get('features_list'), # Save comma-separated list

                # From this form
                confirmed_ownership=confirm,
                # Image handled below
            )

            # Save the image
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            ad.property_image = filename # Save the path relative to MEDIA_ROOT
            ad.save() # Save the PendingAd object to the database

            print("Successfully saved PendingAd:", ad.id, ad.title) # Debugging

            # Clear session data after successful submission
            request.session.pop('rent_basic_info', None)
            request.session.pop('rent_details_info', None)

            # Render success page
            return render(request, 'home/upload_confirm.html', {
                'success': True,
                'image_url': fs.url(filename) # Pass image URL for optional display
            })

        except (ValueError, TypeError, InvalidOperation) as e:
             # Catch potential conversion errors not handled by safe_* functions
             print(f"Data processing error: {e}") # Debugging
             return render(request, 'home/upload_confirm.html', {'error': f'Invalid data submitted. Please check your entries. Error: {e}'})
        except Exception as e: # Catch any other unexpected errors
             print(f"Unexpected error during submission: {e}") # Debugging
             # Log the full traceback here in a real application
             return render(request, 'home/upload_confirm.html', {'error': 'An unexpected error occurred. Please try again later.'})


    # If GET request, show the form
    # Check if previous steps' data exists in session
    if 'rent_basic_info' not in request.session or 'rent_details_info' not in request.session:
        print("Session data missing on GET, redirecting to rent_property") # Debugging
        # Optionally add a message
        return redirect('rent_property')

    return render(request, 'home/upload_confirm.html')


# --- Ensure list_property_details also provides features ---
# (This view seems unused in the rent flow now, but update for consistency if used elsewhere)
def list_property_details(request):
     features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]
     # Add session handling here if this becomes part of a multi-step flow
     return render(request, 'home/list_property_details.html', {'features': features})