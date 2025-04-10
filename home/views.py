from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ConfirmedAd
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render
import os

def home(request):
    return render(request, 'home/home.html')

def list_property(request):
    return render(request, 'home/list_property.html')

def rent_property(request):
    return render(request, 'home/rent_property.html')

def find_a_home(request):
    ads = ConfirmedAd.objects.all().order_by('-id')  # Show latest ads first
    return render(request, 'home/find_a_home.html', {'ads': ads})


    query = request.GET.get('q', '')  # Search keyword
    city = request.GET.get('city', '')
    property_type = request.GET.get('property_type', '')
    bedrooms = request.GET.get('bedrooms', '')
    bathrooms = request.GET.get('bathrooms', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    ads = ConfirmedAd.objects.all()

    # Apply filters
    if query:
        ads = ads.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(features__icontains=query)
        )

    if city:
        ads = ads.filter(city__icontains=city)

    if property_type:
        ads = ads.filter(property_type__icontains=property_type)

    if bedrooms:
        ads = ads.filter(bedrooms=bedrooms)

    if bathrooms:
        ads = ads.filter(bathrooms=bathrooms)

    if min_price:
        ads = ads.filter(price__gte=min_price)

    if max_price:
        ads = ads.filter(price__lte=max_price)

    return render(request, 'home/find_a_home.html', {
        'ads': ads,
        'query': query,
        'city': city,
        'property_type': property_type,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'min_price': min_price,
        'max_price': max_price,
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



