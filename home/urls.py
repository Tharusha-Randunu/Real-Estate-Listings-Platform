from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('find-a-home/', views.find_a_home, name='find_a_home'),
    path('list-property/', views.list_property, name='list_property'),
    path('property/<int:ad_id>/', views.property_detail, name='property_detail'),
    path('rent-property/', views.rent_property, name='rent_property'),
    path('seller-register/', views.seller_register, name='seller_register'),
    path('market-insights/', views.market_insights_page, name='market_insights'),
    path('list/details/', views.list_property_details, name='list_property_details'),
    path('upload_confirm/', views.upload_and_confirm, name='upload_confirm'),
]
