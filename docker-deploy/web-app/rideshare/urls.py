from django.urls import path

from . import views
app_name = "rideshare"
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('driverregister/', views.driverRegister, name='driverregister'),
    path('editdriverinfo/',views.editDriverInfo, name='editdriverinfo'),
    path('rideRequest/',views.rideRequest, name='riderequest')
]