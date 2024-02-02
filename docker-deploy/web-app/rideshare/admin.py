from django.contrib import admin
from .models import Driver, Rider, Ride, RideUser
# Register your models here.
from django.contrib.auth.models import User


admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Ride)
admin.site.register(RideUser)

