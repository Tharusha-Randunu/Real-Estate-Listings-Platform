from . import views

from django.urls import path
from .views import home
from .views import home, list_property
from .views import find_a_home

urlpatterns = [
    path('', home, name='home'),
    path('find-a-home/', find_a_home, name='find_a_home'),
    path('', home, name='home'),
    path('list-property/', list_property, name='list_property'),
    path('property/<int:ad_id>/', views.property_detail, name='property_detail'),
]