from django.db import models

from accounts.models import user
from .manager import ActiveVenueManager


class venue(models.Model):

    owner = models.ForeignKey(
        user,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    is_delete = models.BooleanField(default=False)

    objects = ActiveVenueManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name


class VenueAvailability(models.Model):

    venue = models.ForeignKey(
        venue,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    is_booked = models.BooleanField(default=False)
