from django import forms

from .models import Ride, User
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )


class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat your password', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='LastName', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter a valid email address'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password'}))


class VehicleForm(forms.Form):
    vehicle_type = forms.CharField(
        label='Vehice Type', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    num_passengers = forms.IntegerField( validators=[validate_positive],
        label='Number of passengers', required=True, widget=forms.NumberInput(attrs={'class': 'form-control','type':'number', 'min':'1'}))
    plate = forms.CharField(label='Plate', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    special_vehicle_info = forms.CharField(label='Special vehicle info (optional)', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', required=True,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='New password', required=True,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Repeat your new password', required=True,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditProfileForm(forms.Form):
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='LastName', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class RideRequestForm(forms.Form):
    CHOICES = (
        ('no', 'No'),
        ('yes', 'Yes')
    )
    dest_addr = forms.CharField(label='Destination address', required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    sharable = forms.ChoiceField(label='Wanna share the trip?  ', choices=CHOICES,
                                 required=True, widget=forms.Select())
    num_passengers = forms.IntegerField( validators=[validate_positive],
        label='number of passengers', required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'type':'number', 'min':'1'}))
    vehicle_type = forms.CharField(required=False,
                                   label='vehicle type', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    arrival_time = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        label='arrival date',
        required=True,
        widget=DatePickerInput(
            attrs={'id': 'datepicker', 'autocomplete': 'off'})
    )
    special_request = forms.CharField(required=False,
                                   label='Special request (optional)', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))



class RideDetailForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RideDetailForm, self).__init__(*args, **kwargs)

        self.fields['ride_id'].widget.attrs = {
            'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off'}
        self.fields['owner_email'].widget.attrs = {
            'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off'}
        self.fields['status'].widget.attrs = {
            'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off'}
        self.fields['dest_addr'].widget.attrs['class'] = 'form-control'
        self.fields['arrival_time'].input_formats = ['%Y/%m/%d %H:%M']
        self.fields['arrival_time'].widget.attrs = {'class': 'form-control', 'id': 'id_arrival_time', 'autocomplete': 'off'}
        self.fields['owner_num_passengers'].widget.attrs = {'class': 'form-control', 'autocomplete': 'off', 'type':'number', 'min':'1'}
        self.fields['special_request'].widget.attrs['class'] = 'form-control'

        self.fields['num_passengers'].widget.attrs = {
            'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off'}
        self.fields['driver'].widget.attrs = {'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off',
                                              'placeholder': 'Ride is waiting to be confirmed'}
        self.fields['headcount'].widget.attrs = {'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off',
                                                 'placeholder': 'Ride is waiting to be confirmed'}
        self.fields['vehicle_type'].widget.attrs = {'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off',
                                                    'placeholder': 'Ride is waiting to be confirmed'}
        self.fields['ride_plate'].widget.attrs = {'readonly': 'readonly', 'class': 'form-control', 'autocomplete': 'off',
                                              'placeholder': 'Ride is waiting to be confirmed'}
        self.fields['owner_num_passengers'].validators=[validate_positive]
        self.fields['driver'].required = False
        self.fields['owner_email'].required = False
        self.fields['headcount'].required = False
        self.fields['vehicle_type'].required = False
        self.fields['dest_addr'].required = False
        self.fields['arrival_time'].required = False
        self.fields['ride_id'].required = False
        self.fields['num_passengers'].required = False
        self.fields['owner_num_passengers'].required = False
        self.fields['special_request'].required = False
        self.fields['status'].required = False
        self.fields['ride_plate'].required = False
