from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
import mimetypes
from django.http import HttpResponse
from .models import ConfirmedAd, PropertyFeature, PendingAd, PendingAdImage, ConfirmedAdImage
from decimal import Decimal, InvalidOperation
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import EditProfileForm
from .forms import ConfirmedAdForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordChangeFormCustom
from django.http import JsonResponse
from .models import HousePriceIndex, LandPriceIndex
from collections import defaultdict


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

@login_required(login_url='/login/')
def list_property(request):
    # Attempt to get user profile data (similar to rent_property)
    try:
        user_profile = request.user.userprofile
    except AttributeError:
        messages.warning(request, 'Profile not found. Using default information.')
        user_profile = None

    if request.method == 'POST':
        if user_profile:
            full_name = f"{request.user.first_name} {request.user.last_name}".strip()
            if not full_name:
                full_name = request.user.username
            registration_info = {
                'full_name': full_name,
                'email': request.user.email,
                'contact': getattr(user_profile, 'phone_number', ''),
                'district': request.POST.get('district', ''),
            }
        else:
             registration_info = {
                'full_name': request.user.username,
                'email': request.user.email,
                'contact': '',
                'district': request.POST.get('district', ''),
            }

        if not registration_info['email']:
             messages.error(request, 'User email is missing. Cannot proceed.')
             return render(request, 'home/list_property.html')

        request.session['sell_registration_info'] = registration_info
        print("Saved sell registration info to session:", registration_info)

        basic_info = {
            'user_type': request.POST.get('user_type'),
            'offer_type': request.POST.get('offer_type', 'Sell'), # Default to Sell
            'property_type': request.POST.get('property_type'),
            'city': request.POST.get('city'),
            'street': request.POST.get('street'),
            'latitude': request.POST.get('latitude'),
            'longitude': request.POST.get('longitude'),
        }

        if not all([basic_info['property_type'], basic_info['city']]):
             messages.error(request, 'Property Type and City are required.')
             return render(request, 'home/list_property.html', {'posted_data': request.POST})

        request.session['sell_basic_info'] = basic_info
        print("Saved sell basic info to session:", basic_info)
        return redirect('list_property_details')

    return render(request, 'home/list_property.html')

@login_required(login_url='/login/')
def rent_property(request):
    # --- Step 1: Collect Basic Info & Fetch Profile Data --- (Keep this as it is)
    try:
        user_profile = request.user.userprofile
    except AttributeError:
        messages.warning(request, 'Profile not found. Using default information.')
        user_profile = None

    if request.method == 'POST':
        if user_profile:
            full_name = f"{request.user.first_name} {request.user.last_name}".strip()
            if not full_name:
                full_name = request.user.username
            registration_info = {
                'full_name': full_name,
                'email': request.user.email,
                'contact': getattr(user_profile, 'phone_number', ''),
                'district': request.POST.get('district', ''),
            }
        else:
             registration_info = {
                'full_name': request.user.username,
                'email': request.user.email,
                'contact': '',
                'district': request.POST.get('district', ''),
            }

        if not registration_info['email']:
             messages.error(request, 'User email is missing. Cannot proceed.')
             return render(request, 'home/rent_property.html')

        request.session['rent_registration_info'] = registration_info
        print("Saved rent registration info to session:", registration_info)

        basic_info = {
            'user_type': request.POST.get('user_type'),
            'offer_type': request.POST.get('offer_type', 'Rent'),
            'property_type': request.POST.get('property_type'),
            'city': request.POST.get('city'),
            'street': request.POST.get('street'),
            'latitude': request.POST.get('latitude'),
            'longitude': request.POST.get('longitude'),
        }

        if not all([basic_info['property_type'], basic_info['city']]):
             messages.error(request, 'Property Type and City are required.')
             return render(request, 'home/rent_property.html', {'posted_data': request.POST})

        request.session['rent_basic_info'] = basic_info
        print("Saved rent basic info to session:", basic_info)
        return redirect('rent_property_details')

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

    # Start with all ads and prefetch related images
    ads = ConfirmedAd.objects.all().prefetch_related('images').order_by('-created_at')

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
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

    ads = ads.distinct()

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
    ad = get_object_or_404(ConfirmedAd.objects.prefetch_related('images'), id=ad_id)
    try:
        seller_profile = UserProfile.objects.get(user__email=ad.seller_email)
        seller_profile_pic = seller_profile.profile_picture.url if seller_profile.profile_picture else None
    except UserProfile.DoesNotExist:
        seller_profile_pic = None
    return render(request, 'home/property_detail.html', {'ad': ad, 'seller_profile_pic': seller_profile_pic})

def serve_image(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        with open(media_path, 'rb') as img_file:
            mime_type, _ = mimetypes.guess_type(media_path)
            return HttpResponse(img_file.read(), content_type=mime_type or 'application/octet-stream')
    except FileNotFoundError:
        return HttpResponse(status=404)


def market_insights_page(request):
    return render(request, 'home/market_insights.html')

def agent(request):
    return render(request, 'home/agent.html')

@login_required(login_url='/login/')
def list_property_details(request):
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]

    if 'sell_basic_info' not in request.session:
         print("Sell basic info missing, redirecting to list_property")
         messages.error(request, 'Please complete the property location step first.')
         return redirect('list_property')

    if request.method == 'POST':
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
            'parking': request.POST.get('parking') == 'true' or request.POST.get('parking') == 'on',
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'features_list': request.POST.get('features_list'),
        }

        if not all([details_info['bedrooms'], details_info['bathrooms'], details_info['price'], details_info['title']]):
             messages.error(request, 'Bedrooms, Bathrooms, Price, and Title are required.')
             return render(request, 'home/list_property_details.html', {'features': features, 'posted_data': request.POST})

        request.session['sell_details_info'] = details_info
        print("Saved sell details info to session:", details_info)
        return redirect('upload_confirm')

    return render(request, 'home/list_property_details.html', {'features': features})

@login_required(login_url='/login/')
def rent_property_details(request):
    # --- Step 2: Collect Property Details --- (Keep this as it is)
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]

    if 'rent_basic_info' not in request.session:
         print("Rent basic info missing, redirecting to rent_property")
         messages.error(request, 'Please complete the property location step first.')
         return redirect('rent_property')

    if request.method == 'POST':
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
            'parking': request.POST.get('parking') == 'true' or request.POST.get('parking') == 'on',
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'features_list': request.POST.get('features_list'),
        }

        if not all([details_info['bedrooms'], details_info['bathrooms'], details_info['price'], details_info['title']]):
             messages.error(request, 'Bedrooms, Bathrooms, Price, and Title are required.')
             return render(request, 'home/rent_property_details.html', {'features': features, 'posted_data': request.POST})

        request.session['rent_details_info'] = details_info
        print("Saved rent details info to session:", details_info)
        return redirect('upload_confirm')

    return render(request, 'home/rent_property_details.html', {'features': features})

@login_required(login_url='/login/') # Protect this step
def upload_confirm(request):
    if request.method == 'POST':
        confirm = request.POST.get('confirm') == 'true' or request.POST.get('confirm') == 'on'
        images = request.FILES.getlist('property_images')
        error_msg = None
        registration_info = None
        basic_info = None
        details_info = None
        offer_type = None

        # Determine the flow and retrieve corresponding data
        if 'rent_registration_info' in request.session and 'rent_basic_info' in request.session and 'rent_details_info' in request.session:
            registration_info = request.session.get('rent_registration_info')
            basic_info = request.session.get('rent_basic_info')
            details_info = request.session.get('rent_details_info')
            offer_type = basic_info.get('offer_type', 'Rent')
        elif 'sell_registration_info' in request.session and 'sell_basic_info' in request.session and 'sell_details_info' in request.session:
            registration_info = request.session.get('sell_registration_info')
            basic_info = request.session.get('sell_basic_info')
            details_info = request.session.get('sell_details_info')
            offer_type = basic_info.get('offer_type', 'Sell')
        else:
            messages.error(request, 'Session data is incomplete. Please start the process again.')
            return redirect('home')  # Redirect to the home page or the start of either flow

        # --- Validation ---
        if not registration_info or not basic_info or not details_info:
            error_msg = 'Required information is missing. Please go back and complete all steps.'
        elif not confirm:
            error_msg = 'You must confirm ownership/authorization.'
        elif not images:
            error_msg = 'Please upload at least one property image.'
        elif len(images) > 5:
            error_msg = 'You can upload a maximum of 5 images.'

        if error_msg:
            print("Error during submission:", error_msg)
            messages.error(request, error_msg)
            return render(request, 'home/upload_confirm.html')
        # --- End Validation ---

        try:
            # --- Create PendingAd instance ---
            ad = PendingAd(
                # From registration_info
                registered_name=registration_info.get('full_name', request.user.username),
                registered_email=registration_info.get('email', request.user.email),
                registered_contact=registration_info.get('contact', ''),
                registered_district=registration_info.get('district', ''),

                # From basic_info
                user_type=basic_info.get('user_type'),
                offer_type=offer_type,
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
                features=details_info.get('features_list'),
                confirmed_ownership=confirm, # Ensure this is saved
            )
            # Save the main ad FIRST to get an ID
            ad.save()

            # --- Save Multiple Images ---
            fs = FileSystemStorage() # Or use default storage
            saved_image_urls = []
            for img_file in images:
                # You might want to sanitize filename here before saving
                filename = fs.save(img_file.name, img_file)
                # Create the related image record
                PendingAdImage.objects.create(pending_ad=ad, image=filename)
                saved_image_urls.append(fs.url(filename)) # Store URL if needed

            print(f"Successfully saved PendingAd (Offer Type: {offer_type}):", ad.id, ad.title)
            print(f"Saved {len(saved_image_urls)} images.")

            # Clear session data based on the flow
            if offer_type == 'Rent':
                request.session.pop('rent_registration_info', None)
                request.session.pop('rent_basic_info', None)
                request.session.pop('rent_details_info', None)
            elif offer_type == 'Sell':
                request.session.pop('sell_registration_info', None)
                request.session.pop('sell_basic_info', None)
                request.session.pop('sell_details_info', None)

            messages.success(request, f"Your ad '{ad.title}' for {offer_type} has been submitted for review!")

            return render(request, 'home/upload_confirm.html', {'success': True})

        except (ValueError, TypeError, InvalidOperation) as e:
            print(f"Data processing error: {e}")
            messages.error(request, f'Invalid data submitted. Please check your entries. Error: {e}')
            return render(request, 'home/upload_confirm.html')
        except Exception as e:
            print(f"Unexpected error during submission: {e}")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'home/upload_confirm.html')

    # --- If GET request, show the form ---
    rent_data_present = all(key in request.session for key in ['rent_registration_info', 'rent_basic_info', 'rent_details_info'])
    sell_data_present = all(key in request.session for key in ['sell_registration_info', 'sell_basic_info', 'sell_details_info'])

    if not rent_data_present and not sell_data_present:
        messages.error(request, 'Please start the process from the beginning.')
        return redirect('home')  # Redirect to the home page

    return render(request, 'home/upload_confirm.html')

def our_services(request):
    return render(request, 'home/our_services.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # <-- include request.FILES
        if form.is_valid():
            user, profile = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form}) # Directly in the 'home' folder

@login_required
def dashboard(request):
    user_ads = ConfirmedAd.objects.filter(seller_email=request.user.email).order_by('-created_at')

    # Prefetch related images to avoid multiple database queries in the template
    user_ads = user_ads.prefetch_related('confirmedadimage_set')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'user_ads': user_ads,
        'user_profile': user_profile,
    }
    return render(request, 'home/dashboard/dashboard.html', context)

def user_logout(request):
    logout(request)
    return redirect('home') # Make sure you have a URL named 'home'


@login_required
def dashboard(request):
    user_ads = ConfirmedAd.objects.filter(seller_email=request.user.email).order_by('-created_at')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'user_ads': user_ads,
        'user_profile': user_profile,
    }
    return render(request, 'home/dashboard/dashboard.html', context)

@login_required
def edit_profile(request):
    # Get the user's profile (assuming a one-to-one relationship between User and UserProfile)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the form data
            return redirect('dashboard')  # Redirect to the dashboard or any page you prefer
    else:
        form = EditProfileForm(instance=user_profile)

    return render(request, 'home/edit_profile.html', {'form': form})




from django.shortcuts import render, get_object_or_404, redirect
from .models import ConfirmedAd
from .forms import ConfirmedAdForm

def edit_ad(request, ad_id):
    print(f"Received ad_id: {ad_id}")  # Debugging line

    ad = get_object_or_404(ConfirmedAd, id=ad_id)

    if request.method == 'POST':
        form = ConfirmedAdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you go after saving
    else:
        form = ConfirmedAdForm(instance=ad)

    return render(request, 'home/edit_ad.html', {'form': form})



def delete_ad(request, ad_id):
    print("Delete view triggered")
    ad = get_object_or_404(ConfirmedAd, id=ad_id)

    # Optional: restrict to owner
    if request.user.email != ad.seller_email:
        messages.error(request, "You don't have permission to delete this ad.")
        return redirect('dashboard')

    ad.delete()
    messages.success(request, "Advertisement deleted successfully.")
    return redirect('dashboard')




def help_page(request):
    return render(request, 'home/help.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeFormCustom(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('dashboard')  # Redirect to the dashboard or any page you prefer
        else:
            messages.error(request, 'There was an error with your password change. Please check your input.')
    else:
        form = PasswordChangeFormCustom(user=request.user)

    return render(request, 'home/change_password.html', {'form': form})



def house_price_data(request):
    data = HousePriceIndex.objects.all().order_by('quarter')
    chart_data = defaultdict(list)
    labels = sorted(set(data.values_list('quarter', flat=True)))

    for record in data:
        chart_data[record.region].append((record.quarter, record.price_index))

    datasets = []
    colors = ['#1e88e5', '#43a047', '#ff5722', '#6a1b9a']  # extend as needed
    for i, (region, values) in enumerate(chart_data.items()):
        values_dict = dict(values)
        datasets.append({
            'label': region,
            'data': [values_dict.get(q, None) for q in labels],
            'borderColor': colors[i % len(colors)],
            'tension': 0.4
        })

    return JsonResponse({'labels': labels, 'datasets': datasets})


def land_price_data(request):
    data = LandPriceIndex.objects.all().order_by('quarter')
    chart_data = defaultdict(list)
    labels = sorted(set(data.values_list('quarter', flat=True)))

    for record in data:
        chart_data[record.city].append((record.quarter, record.price_index))

    datasets = []
    colors = ['#d32f2f', '#388e3c', '#fbc02d', '#1976d2']  # extend as needed
    for i, (city, values) in enumerate(chart_data.items()):
        values_dict = dict(values)
        datasets.append({
            'label': city,
            'data': [values_dict.get(q, None) for q in labels],
            'borderColor': colors[i % len(colors)],
            'tension': 0.4
        })

    return JsonResponse({'labels': labels, 'datasets': datasets})