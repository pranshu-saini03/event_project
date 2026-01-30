from django.contrib import admin
from .models import user, OwnerPermission, permission


admin.site.register(user)
admin.site.register(permission)
admin.site.register(OwnerPermission)
# Register your models here.
