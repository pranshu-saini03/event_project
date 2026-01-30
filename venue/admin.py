from django.contrib import admin

from .models import venue, VenueAvailability


admin.site.register(venue)
admin.site.register(VenueAvailability)
