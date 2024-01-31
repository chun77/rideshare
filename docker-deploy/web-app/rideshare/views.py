from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.http import Http404
from django.views import generic

from django.shortcuts import render, get_object_or_404


class IndexView(generic.ListView):
    template_name = "rideshare/index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.all()

class DetailView(generic.DetailView):
    model = User
    template_name = "rideshare/detail.html"

