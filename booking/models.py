from django.db import models
from accounts.models import user
from venue.models import venue
# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    venue = models.ForeignKey(venue, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20,default='booked')
