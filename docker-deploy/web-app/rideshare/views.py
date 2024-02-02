from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import Http404
from django.views import generic
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

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
def home(request):
	users = User.objects.all()


	context = {'user_list':users}

	return render(request, 'rideshare/home.html', context)

# class DetailView(generic.DetailView):
#     model = User
#     context_object_name = 'user'
#     template_name = "rideshare/detail.html"

