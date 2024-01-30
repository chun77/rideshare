from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404

def index(request):
    user_list = User.objects.all()
    context = {
        "user_list": user_list,
    }
    return render(request, "rideshare/index.html", context)

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, "rideshare/detail.html", {"user": user})
