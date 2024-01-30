from django.contrib import admin
from .models import User, Driver, Rider, Ride, RideUser
# Register your models here.
admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Ride)
admin.site.register(RideUser)
