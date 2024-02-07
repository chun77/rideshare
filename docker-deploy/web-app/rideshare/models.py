from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def get_default_user():
    return User.object.get(name='default')

# class User(models.Model):
#     first_name_text = models.CharField(max_length=200)
#     last_name_text = models.CharField(max_length=200)
#     password_text = models.CharField(max_length=200)

#     def __str__(self):
#         return f'({self.first_name_text}, {self.last_name_text})'

# class User(User):
#     def __str__(self):
#         return f'({self.first_name}, {self.last_name}, {self.email})'

def get_default_driver():
    return Driver.object.get(name='default')

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=200)
    max_passengers = models.IntegerField(null=True)
    plate_number = models.CharField(max_length=200)
    special_info = models.TextField(blank=True)

    def __str__(self):
        return f'({self.user}, {self.vehicle_type}, {self.max_passengers}, {self.plate_number}, {self.special_info})'



# class Rider(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f'{self.user}'


class Ride(models.Model):
    # ride_id = models.BigAutoField()
    # this should be either complete, confirmed, open
    status = models.CharField(max_length=200)
    # need a start location and end location
    end_loc = models.CharField(max_length=200)
    arrival_time = models.DateTimeField("arrival time",null=True)
    num_passengers = models.BigIntegerField(null=True)
    shareable = models.BooleanField(default = True)
    driver_user = models.ForeignKey(Driver, on_delete=models.CASCADE,null=True,blank = True)
    request_user = models.ForeignKey(User, on_delete=models.CASCADE)
    special_info = models.TextField(blank=True)

    # def __str__(self):
    #     return f'({self.status}, {self.driver_user}, {self.request_user}, {self.ride_id})'


# share form? -> session save ? cache
# join -> save to database

# only sharer? -> nope
class RideUser(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_party = models.BigIntegerField(null=True)
    
    # def __str__(self):
    #     return f'({self.user}, {self.ride})'
