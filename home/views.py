from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home/home.html')
def list_property(request):
    return render(request, 'home/list_property.html')
