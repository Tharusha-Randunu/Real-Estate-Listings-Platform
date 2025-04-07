from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Real Estate Listings</h1>")
    return HttpResponse("<h1>Group 5</h1>")
