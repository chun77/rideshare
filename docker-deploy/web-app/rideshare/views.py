from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.views import generic
from django.contrib import messages
from .forms import CreateUserForm, CreateDriverForm, CreateRideForm
from django.contrib.auth import authenticate, login, logout
from .models import Driver, Ride, RideUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from datetime import datetime


# class IndexView(generic.ListView):
#     template_name = "rideshare/index.html"
#     context_object_name = "user_list"

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return OurUser.objects.all()

# @login_required(login_url='rideshare:login')
# class DriverUpdateView(UpdateView):
# 	def __init__(self,model,fields,template):
# 		model = Driver
# 		fields = ['vehicle_type', 'max_passengers', 'plate_number', 'special_info']
# 		template = "editDriverInfo"

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('rideshare:home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('rideshare:login')
			

		context = {'form':form}
		return render(request, 'rideshare/register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('rideshare:home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('rideshare:home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'rideshare/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('rideshare:login')

@login_required(login_url='rideshare:login')
def driverRegister(request):
	# initial_data = {'user': request.user}
	form = CreateDriverForm()
	
	if request.method == 'POST':
		form = CreateDriverForm(request.POST)
		print('vehicle type')
		# print(form.fields['vehicle_type'].)
		# form.fields['user'] = request.user
		if form.is_valid():

			driver = form.save(commit=False)
			driver.user = request.user
			driver.save()
			return redirect('rideshare:home')
	driver_context = {'form': form}
	return render(request, 'rideshare/driverRegister.html', driver_context)

@login_required(login_url='rideshare:login')
def editDriverInfo(request):
	driver = get_object_or_404(Driver, user = request.user)
	if request.method == 'GET':
		context = {'form': CreateDriverForm(instance=driver)}
		return render(request,'rideshare/editDriverInfo.html',context)
	elif request.method == 'POST':
		form = CreateDriverForm(request.POST, instance=driver)
		if form.is_valid():
			form.save()
			return redirect('rideshare:home')
		else:
			messages.error(request, 'Please correct the following errors:')
			return render(request,'rideshare/editDriverInfo.html',{'form':form})


@login_required(login_url='rideshare:login')
def home(request):
	context = {}
	
	context['isDriver'] = Driver.objects.filter(user=request.user).exists()
	return render(request, 'rideshare/home.html', context)

@login_required(login_url='rideshare:login')
def rideRequest(request):
	form = CreateRideForm()
	
	if request.method == 'POST':
		form = CreateRideForm(request.POST)
		if form.is_valid():
			

			ride = form.save(commit=False)

			date_str = request.POST['d']  # e.g., '2024-02-03'
			time_str = request.POST['e']  # e.g., '14:30'
			# Combine the date and time strings into a datetime object
			ride.arrival_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
			
    
			ride.status = "OPEN"
			ride.request_user = request.user
			ride.save()
			rideuser = RideUser.objects.create(ride = ride,
								user = request.user, 
								num_party = ride.num_passengers)
			rideuser.save()
			return redirect('rideshare:home')
	context = {'form': form}
	return render(request, 'rideshare/rideRequest.html', context)