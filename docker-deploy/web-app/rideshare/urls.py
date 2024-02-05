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
    path('rideRequest/',views.rideRequest, name='riderequest'),
    path('viewnoncomplete/',views.viewNonComplete, name='viewnoncomplete'),
    path('<int:ride_id>/viewridedetails/', views.viewRideDetails, name='viewridedetails'),
    path('<int:ride_id>/viewdriverdetails/', views.viewDriverDetails, name='viewdriverdetails'),
    path('searchforride/', views.searchForRide, name='searchforride'),
    path('showsearchresults/', views.showSearchResults, name='showsearchresults'),
    path('<int:ride_id>/editridedetails/', views.editRideDetails, name='editridedetails')

]