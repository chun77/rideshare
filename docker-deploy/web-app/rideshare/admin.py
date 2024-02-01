from django.contrib import admin
from .models import User, Driver, Rider, Ride, RideUser
# Register your models here.

admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Ride)
admin.site.register(RideUser)

class UserAdmin(admin.ModelAdmin):
    fields = ["first_name_text", "last_name_text"]
    list_display = ["first_name_text", "last_name_text"]
    search_fields = ["first_name_text", "last_name_text"]

admin.site.register(User, UserAdmin)