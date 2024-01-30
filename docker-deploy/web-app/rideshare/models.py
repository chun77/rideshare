from django.db import models

# Create your models here.

def get_default_user():
    return User.object.get(name='default')

class User(models.Model):
    first_name_text = models.CharField(max_length=200)
    last_name_text = models.CharField(max_length=200)
    password_text = models.CharField(max_length=200)

def get_default_driver():
    return Driver.object.get(name='default')

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_default_user))
    vehicle_type = models.CharField(max_length=200)
    max_passengers = models.IntegerField()
    plate_number = models.CharField(max_length=200)
    special_info = models.TextField()

def get_default_rider():
    return Rider.object.get(name='default')

class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Ride(models.Model):
    ride_id = models.BigIntegerField()
    # this should be either complete, confirmed, open
    status = models.CharField(max_length=200)
    # need a start location and end location
    start_loc = models.CharField(max_length=200)
    end_loc = models.CharField(max_length=200)
    create_time = models.DateTimeField("time created")
    end_time = models.DateTimeField("time completed")
    driver_user = models.ForeignKey(Driver, on_delete=models.SET(get_default_driver))
    request_user = models.ForeignKey(Rider, on_delete=models.SET(get_default_rider))


class RideUser(models.Model):
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
