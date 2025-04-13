from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
import mimetypes
from decimal import Decimal

from .models import ConfirmedAd, PropertyFeature, PendingAd

def home(request):
    latest_ads = ConfirmedAd.objects.order_by('-id')[:10]
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
    if features:
        ads = ads.filter(property_features__name__in=features).distinct()

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

def upload_confirm(request):
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        image = request.FILES.get('property_image')

        if not confirm:
            return render(request, 'home/upload_confirm.html', {'error': 'You must confirm ownership.'})
        if not image:
            return render(request, 'home/upload_confirm.html', {'error': 'Please upload a property image.'})

        basic_info = request.session.get('basic_info')
        details_info = request.session.get('details_info')

        if not basic_info or not details_info:
            return render(request, 'home/upload_confirm.html', {'error': 'Session expired or data missing. Please restart the ad submission.'})

        try:
            price = details_info.get('price')
            ad = PendingAd(
                city=basic_info.get('city'),
                street=basic_info.get('street'),
                latitude=float(basic_info.get('latitude')) if basic_info.get('latitude') else None,
                longitude=float(basic_info.get('longitude')) if basic_info.get('longitude') else None,
                bedrooms=int(details_info.get('bedrooms')),
                bathrooms=int(details_info.get('bathrooms')),
                floor_area=int(details_info.get('floor_area')),
                price=Decimal(price) if price else None,
                price_type=details_info.get('price_type'),
                title=details_info.get('title'),
                description=details_info.get('description'),
            )

            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            ad.property_image = filename
            ad.save()

            request.session.pop('basic_info', None)
            request.session.pop('details_info', None)

            return render(request, 'home/upload_confirm.html', {
                'success': True,
                'image_url': fs.url(filename)
            })

        except (ValueError, TypeError) as e:
            return render(request, 'home/upload_confirm.html', {'error': f'Data error: {e}'})

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
