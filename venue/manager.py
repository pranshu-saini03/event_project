from django.db import models


class ActiveVenueManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)
