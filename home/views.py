from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ConfirmedAd
from django.conf.urls.static import static
from django.conf import settings
import os

def home(request):
    return render(request, 'home/home.html')
def list_property(request):
    return render(request, 'home/list_property.html')



def find_a_home(request):
    ads = ConfirmedAd.objects.all().order_by('-id')  # Show latest ads first
    return render(request, 'home/find_a_home.html', {'ads': ads})

def property_detail(request, ad_id):
    ad = get_object_or_404(ConfirmedAd, id=ad_id)

    # Pass the property ad to the template
    return render(request, 'home/property_detail.html', {'ad': ad})




def serve_image(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        with open(media_path, 'rb') as img_file:
            return HttpResponse(img_file.read(), content_type='image/jpeg')
    except FileNotFoundError:
        return HttpResponse(status=404)