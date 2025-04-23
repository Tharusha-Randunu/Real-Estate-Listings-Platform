from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('find-a-home/', views.find_a_home, name='find_a_home'),
    path('list-property/', views.list_property, name='list_property'),
    path('property/<int:ad_id>/', views.property_detail, name='property_detail'),
    path('rent-property/', views.rent_property, name='rent_property'),
    path('market-insights/', views.market_insights_page, name='market_insights'),
    path('list/details/', views.list_property_details, name='list_property_details'),
    path('upload_confirm/', views.upload_confirm, name='upload_confirm'),
    path('rent-property/details/', views.rent_property_details, name='rent_property_details'),
    path('agent/', views.agent, name='agent'),
    path('our-services/', views.our_services, name='our_services'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit-ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete-ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),



]

# Media files for development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
