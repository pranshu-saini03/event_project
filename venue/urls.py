from django.urls import path
from .views import create_venue, list_venues, add_availability,update_venue, delete_venue
urlpatterns = [
    path('create/', create_venue, name='create_venue'),
    path('list/', list_venues, name='list_venues'),
    path('update/', update_venue, name='update_venue'),
    path('delete/', delete_venue, name='delete_venue'),
    path('add_availability/', add_availability, name='add_availability'),
]