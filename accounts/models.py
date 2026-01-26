from django.db import models
class user(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('user', 'User'),
    )
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return self.username
class permission(models.Model):
    create=models.BooleanField(default=False)
    read=models.BooleanField(default=False)
    update=models.BooleanField(default=False)
    delete= models.BooleanField(default=False)

class OwnerPermission(models.Model):
    owner = models.ForeignKey(user, on_delete=models.CASCADE)
    permission = models.ForeignKey(permission, on_delete=models.CASCADE)
# Create your models here.
