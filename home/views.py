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



