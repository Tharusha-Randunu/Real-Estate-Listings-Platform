from django.urls import path
from .views import home
from .views import home, list_property


urlpatterns = [
    path('', home, name='home'),
]

urlpatterns = [
    path('', home, name='home'),
    path('list-property/', list_property, name='list_property'),
]


