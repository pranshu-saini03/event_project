from django.db import models
from accounts.models import user


class venue(models.Model):
    owner=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class VenueAvailability(models.Model):
    venue = models.ForeignKey(venue, on_delete=models.CASCADE)
    date = models.DateField()
    is_booked = models.BooleanField(default=False)
# Create your models here.
