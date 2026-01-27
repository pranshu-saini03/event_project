from django.urls import path
from .views import create_venue, list_venues, add_availability
urlpatterns = [
    path('create/', create_venue, name='create_venue'),
    path('list/', list_venues, name='list_venues'),
    path('add_availability/', add_availability, name='add_availability'),
]