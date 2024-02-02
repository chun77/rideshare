from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.views import generic
from django.contrib import messages
from .forms import CreateUserForm, CreateDriverForm
from django.contrib.auth import authenticate, login, logout
from .models import Driver, Ride, Rider, RideUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


# class IndexView(generic.ListView):
#     template_name = "rideshare/index.html"
#     context_object_name = "user_list"

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return OurUser.objects.all()

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
	initial_data = {'user': request.user}
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
def home(request):
	context = {}
	
	context['isDriver'] = Driver.objects.filter(user=request.user).exists()
	return render(request, 'rideshare/home.html', context)

