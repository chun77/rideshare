from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.views import generic
from django import forms
from django.contrib import messages
from .forms import CreateUserForm, CreateDriverForm, CreateRideForm
from django.contrib.auth import authenticate, login, logout
from .models import Driver, Ride, RideUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from datetime import datetime
from django.db.models import Q

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

@login_required(login_url='rideshare:login')
def viewNonComplete(request):
	results = RideUser.objects.filter(user = request.user).select_related('ride').exclude(ride__status = "COMPLETE")
	context = {}
	context['object_list'] = results
	# context['driver_name'] = 

	return render(request, 'rideshare/viewNonComplete.html', context)

@login_required(login_url='rideshare:login')
def viewRideDetails(request, ride_id):
	ride = get_object_or_404(Ride, pk=ride_id)

	ride_form = CreateRideForm(instance=ride)
	ride_form.fields['status'] = forms.CharField(initial=ride.status)
	ride_form.fields['arrival_time'] = forms.DateTimeField(initial=ride.arrival_time)
	ride_form.fields['ride_owner'] = forms.CharField(initial=ride.request_user.username)
	for field in ride_form.fields:
		ride_form.fields[field].widget.attrs['readonly'] = True
	ride_form.fields['shareable'].widget.attrs['disabled'] = True

	context = {'ride_form': ride_form}
	return render(request, 'rideshare/viewRideDetails.html', context)


@login_required(login_url='rideshare:login')
def viewDriverDetails(request, ride_id):
	ride = get_object_or_404(Ride, pk=ride_id)
	
	driver = ride.driver_user
	driver_form = CreateDriverForm(instance=driver)
	driver_form.fields['driver_name'] = forms.CharField(initial=driver.user.username)
	for field in driver_form.fields:
		driver_form.fields[field].widget.attrs['readonly'] = True
	context = {'driver_form': driver_form}
	
		# context[field.name] = driver[field]
	print(driver.max_passengers)
	return render(request, 'rideshare/viewDriverDetails.html', context)

@login_required(login_url='rideshare:login')
def searchForRide(request):
	form = CreateRideForm()
	# form.fields['arrival_time_latest'] = forms.DateTimeField()
	# form.fields['arrival_time_earliest'] = forms.DateTimeField()
	if request.method == 'POST':
		form = CreateRideForm(request.POST)
		# form.fields['shareable'] = True
		if form.is_valid():
			

			ride = form.save(commit=False)

			date_str = request.POST['d']  # e.g., '2024-02-03'
			time_str = request.POST['e']  # e.g., '14:30'
			# Combine the date and time strings into a datetime object
			# ride.arrival_time_earliest = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')

			date_str2 = request.POST['f']  # e.g., '2024-02-03'
			time_str2 = request.POST['g']  # e.g., '14:30'
			# Combine the date and time strings into a datetime object
			# ride.arrival_time_latest = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
			
    
			ride.status = "OPEN"
			ride.request_user = request.user
			request.session['destination_address'] = ride.end_loc
			request.session['early_date'] = date_str
			request.session['early_time'] = time_str
			request.session['late_date'] = date_str2
			request.session['late_time'] = time_str2
			# request.session['late'] = ride.arrival_time_latest
			request.session['num_passengers'] = ride.num_passengers
			request.session['special_info'] = ride.special_info
			return redirect('rideshare:showsearchresults')
	
	context = {'form': form}
	return render(request, 'rideshare/searchForRide.html', context)

@login_required(login_url='rideshare:login')
def showSearchResults(request):
	early_arrival = datetime.strptime(f"{request.session['early_date']} {request.session['early_time']}", '%Y-%m-%d %H:%M')
	print(early_arrival)
	late_arrival = datetime.strptime(f"{request.session['late_date']} {request.session['late_time']}", '%Y-%m-%d %H:%M')
	result = RideUser.objects.exclude(user = request.user).select_related("ride").filter(
								Q(ride__end_loc = request.session['destination_address']) 
							  & Q(ride__special_info = request.session['special_info'])
							  & Q(ride__arrival_time__gte = early_arrival)
							  & Q(ride__arrival_time__lte = late_arrival)
							  & Q(ride__shareable = True)
							  & Q(ride__status = 'OPEN'))
	if request.method == 'POST':
		# need to know which option they chose
		ride_id = request.POST.get('ride_id')
		# once we know, we can incrememt the ride by the amount of passengers
		num_party = request.session['num_passengers']
		ride = Ride.objects.get(id = ride_id)
		ride.num_passengers += num_party
		ride.save()
		
		# can also make a new entry in the RideUser database wit
		rideuser = RideUser.objects.create(ride=ride, user=request.user,num_party = num_party)
		rideuser.save()
		return redirect('rideshare:home')

	context = {'result': result}
	return render(request, 'rideshare/showSearchResults.html', context)

@login_required(login_url='rideshare:login')
def editRideDetails(request, ride_id):
	context = {}
	context['shared'] = True
	ride_obj = get_object_or_404(Ride, pk=ride_id)
	rideuser = RideUser.objects.get(Q(user = request.user)
												& Q(ride = ride_obj))
	
	if ride_obj.request_user != request.user:
		context['is_owner'] = False
	else:
		context['is_owner'] = True
		ride_result = RideUser.objects.exclude(user = request.user).filter(ride = ride_obj)
		if not ride_result:
			context['shared'] = False

	ride_form = CreateRideForm(instance= ride_obj)
	ride_form.fields["arrival_time"] = forms.DateTimeField(initial=ride_obj.arrival_time)
	# change this later
	ride_form.fields["num_party"] = forms.IntegerField(initial=rideuser.num_party)
	ride_form.fields['ride_owner'] = forms.CharField(initial=ride_obj.request_user.username)

	# ride_form.fields['ride_owner'].widget.attrs['readonly'] = True
	# if not context['is_owner'] or context['shared']:
	# 	ride_form.fields['shareable'].widget.attrs['disabled'] = True
	# 	for field in ride_form.fields:
	# 		if field != 'num_party':
	# 			ride_form.fields[field].widget.attrs['readonly'] = True
				
	# else:
	# 	if context['shared']:
	# 		ride_form.fields['shareable'].widget.attrs['disabled'] = True
	# 		for field in ride_form.fields:
	# 			if field != 'num_party':
	# 				ride_form.fields[field].widget.attrs['readonly'] = True
					
	context['ride_form'] = ride_form
	if request.method == "GET":
		return render(request, 'rideshare/editRideDetails.html', context)
	elif request.method == "POST":
		if request.POST.get('leave') == "Leave Ride":
			print('here')
			if context['is_owner']:
				ride_obj.delete()
			else:
				ride_obj.num_passengers -= rideuser.num_party
				ride_obj.save()
			rideuser.delete()
		else:
			# check time
			# if time in range only when owner and shared
			if request.POST.get('num_party') == '':
				num_party = rideuser.num_party
			else:
				num_party = int(request.POST.get('num_party'))
			if context['is_owner'] and not context['shared']:
				print(request.POST.get('special_info'))
				if request.POST.get('arrival_time') != None:
					ride_obj.arrival_time = request.POST.get('arrival_time')
				if request.POST.get('shareable') != None:
					if request.POST.get('shareable') == 'on':
						ride_obj.shareable = True
					else:
						ride_obj.shareable = False
				if request.POST.get('special_info') != '':
					ride_obj.special_info = request.POST.get('special_info')
				if request.POST.get('end_loc') != '':
					ride_obj.end_loc = request.POST.get('end_loc')
				ride_obj.num_passengers = num_party
			else:
				print(num_party)
				ride_obj.num_passengers = ride_obj.num_passengers - rideuser.num_party + num_party
			ride_obj.save()

			rideuser.num_party = num_party
			rideuser.save()
			
		return redirect("rideshare:home")
