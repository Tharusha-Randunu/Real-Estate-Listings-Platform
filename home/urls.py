from django.urls import path
from .views import home, list_property, rent_property

urlpatterns = [
    path('', home, name='home'),
    path('list-property/', list_property, name='list_property'),
    path('rent-property/', rent_property, name='rent_property'),
]





