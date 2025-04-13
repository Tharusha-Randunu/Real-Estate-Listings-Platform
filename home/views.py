from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ConfirmedAd, PropertyFeature
from django.conf import settings
import os
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

def home(request):
    latest_ads = ConfirmedAd.objects.order_by('-id')[:4]  # Fetch the latest 10 ads
    return render(request, 'home/home.html', {'latest_ads': latest_ads})

def list_property(request):
    return render(request, 'home/list_property.html')

def rent_property(request):
    return render(request, 'home/rent_property.html')

def find_a_home(request):
    # Get filter parameters from the GET request
    query = request.GET.get('q', '')  # Search by keyword
    city = request.GET.get('city', '')
    property_type = request.GET.get('property_type', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    features = request.GET.getlist('features', [])  # List of selected features
    offer_type = request.GET.get('offer_type',)  # Default to 'Sale' if not specified

    # Start with all ads
    ads = ConfirmedAd.objects.all()

    # Apply filters based on the query parameters
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
        ads = ads.filter(offer_type=offer_type)  # Apply filtering for offer type (Sale/Rent)

    # Apply filtering for features (many-to-many relationship)
    if features:
        ads = ads.filter(property_features__in=features)

    # Get the available features for the filter dropdown
    available_features = PropertyFeature.objects.all()

    return render(request, 'home/find_a_home.html', {
        'ads': ads,
        'query': query,
        'city': city,
        'property_type': property_type,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'min_price': min_price,
        'max_price': max_price,
        'available_features': available_features,
        'selected_features': features,
        'offer_type': offer_type,  # Pass the offer_type to the template for form persistence
    })

def property_detail(request, ad_id):
    ad = get_object_or_404(ConfirmedAd, id=ad_id)
    return render(request, 'home/property_detail.html', {'ad': ad})

def serve_image(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        with open(media_path, 'rb') as img_file:
            return HttpResponse(img_file.read(), content_type='image/jpeg')
    except FileNotFoundError:
        return HttpResponse(status=404)

def seller_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        district = request.POST.get('district')

        # You can save to DB later – just printing for now
        print(f"Name: {full_name}, Email: {email}, Contact: {contact}, District: {district}")

        return render(request, 'home/list_property.html')  # redirect to listing form

    return render(request, 'home/seller_register.html')

def market_insights_page(request):
    return render(request, 'home/market_insights.html')

def list_property_details(request):
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]
    return render(request, 'home/list_property_details.html', {'features': features})

def upload_and_confirm(request):
    if request.method == 'POST' and request.FILES.get('property_image'):
        image = request.FILES['property_image']
        confirm = request.POST.get('confirm')

        if not confirm:
            return render(request, 'home/upload_confirm.html', {
                'error': 'Please confirm ownership.'
            })

        # Save image to media folder
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        return render(request, 'home/upload_confirm.html', {
            'success': True,
            'image_url': uploaded_file_url
        })

    return render(request, 'home/upload_confirm.html')

def rent_property_details(request):
    features = [
        "AC Rooms", "Indoor Garden", "Swimming Pool", "Waterfront/Riverside", "Beachfront",
        "Gated Community", "Rooftop Garden", "Lawn Garden", "Luxury Specification", "Brand New",
        "24 Hours Security", "Maid's Room", "Maid's Toilet", "Hot Water", "Attached Toilets",
        "Infinity Pool", "Garage"
    ]
    return render(request, 'home/rent_property_details.html', {'features': features})

def agent_list(request):
    return render(request, 'home/agent.html')
