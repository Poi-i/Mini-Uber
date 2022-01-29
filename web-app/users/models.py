from enum import unique
from tabnanny import verbose
from django.db import models
from django.forms import widgets
from django.utils.timezone import now


# Create your models here.
class User(models.Model):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True, default='')
    password = models.CharField(verbose_name='password', max_length=20)
    create_date = models.DateTimeField(default=now, editable=False)
    last_update_date = models.DateTimeField(auto_now=True, editable=False)
    driver = models.BooleanField(verbose_name='if this user is a driver', default=False, editable=False)
    firstname = models.CharField(verbose_name='firstname', max_length=100, default='')
    lastname = models.CharField(verbose_name='lastname', max_length=100, default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'

class Driver_Car(models.Model):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True, default='')
    plate = models.CharField(verbose_name="licence plate number", max_length=100, unique=True, default='')

    def __str__(self) -> str:
        return self.email + '+' + self.plate
    
    class Meta:
        verbose_name = 'Driver_Car'

class Vehicle(models.Model):
    plate = models.CharField(verbose_name="licence plate number", max_length=100, unique=True, default='')
    vehicle_type = models.CharField(verbose_name="vehicle type", max_length=100, default='')
    num_passengers = models.IntegerField(verbose_name="vehicle capacity", default=0)
    special_vehicle_info = models.TextField(verbose_name="special vehicle info", blank = True, default = '')
    def __str__(self) -> str:
        return self.plate

    class Meta:
        verbose_name = 'Vehicle'

class Ride(models.Model):
    ride_id = models.CharField(primary_key=True, verbose_name='ride order id', max_length=100)
    owner_email = models.EmailField(verbose_name='ride owner email', max_length=100, default='')
    driver = models.EmailField(verbose_name='driver email', max_length=100, default='')
    dest_addr = models.CharField(verbose_name='destination address', max_length=100,default='')
    arrival_time = models.DateTimeField(verbose_name='arrival time')
    headcount = models.CharField(verbose_name="left capacity", default='', max_length=100)
    sharable = models.BooleanField(verbose_name="share or not", default='no')
    status = models.CharField(verbose_name='status', max_length=20, default='open')
    vehicle_type = models.CharField(verbose_name='vehicle type', max_length=100)
    ride_plate = models.CharField(verbose_name='vehicle plate', max_length=100, blank = True, default = '')
    create_date = models.DateTimeField(default=now, editable=False)
    num_passengers = models.IntegerField(verbose_name="passengers number of this ride", default=0)
    owner_num_passengers = models.IntegerField(verbose_name="Your party passengers number of this ride", default=0)
    special_request = models.TextField(verbose_name="special request of this ride", blank = True, default = '')
    

    def __str__(self) -> str:
        return self.ride_id

    class Meta:
        verbose_name = 'Ride'

class Ride_Passenger(models.Model):
    ride_id = models.CharField(verbose_name='ride id', editable=False, max_length=50)
    email = models.EmailField(verbose_name='all passengers email,', max_length=100, default='')
    party_num_passengers = models.IntegerField(verbose_name='party number of passengers', default=0)
    role = models.CharField(verbose_name='owner or sharer or driver', max_length=50, default='')

    def __str__(self) -> str:
        return self.ride_id

    class Meta:
        verbose_name = 'Ride_Passenger'