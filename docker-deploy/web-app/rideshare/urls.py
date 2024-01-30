from django.urls import path

from . import views
app_name = "rideshare"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:user_id>/", views.detail, name="detail"),
]