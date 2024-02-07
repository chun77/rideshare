from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Driver,Ride

class CreateDriverForm(ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	self.request = kwargs.pop("request")
	# 	super(CreateDriverForm, self).__init__(*args, **kwargs)
	# 	self.fields['user'] = self.request.user
	class Meta:
		model = Driver
		fields = ['vehicle_type', 'max_passengers', 'plate_number', 'special_info']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateRideForm(ModelForm):
	class Meta:
		model = Ride
		fields = ['end_loc','num_passengers','shareable','special_info']
