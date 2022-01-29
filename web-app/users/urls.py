from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login,name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('driver-register/', views.driver_register, name='driver_register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('ride-request/', views.ride_request, name='ride_request'),
    path('ride-detail/<slug:slug>/', views.ride_detail, name='ride_detail'),
    path('confirm-ride-detail/<slug:slug>/', views.confirm_ride_detail, name='confirm_ride_detail')
    # path('send_email/', views.send_email, name='send_email')
]
