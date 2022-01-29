from wsgiref.util import request_uri
from django.db import reset_queries
from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse, reverse_lazy
from .models import Ride, User, Vehicle, Driver_Car, Ride_Passenger
from . import forms
from django.conf import settings  # 将settings的内容引进
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # 这样可以发送HTML格式的内容了
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q
from django.db import transaction

import uuid


def edit_profile(request):
    if 'email' not in request.session:
        return redirect('/login')
    user = User.objects.get(email=request.session['email'])
    if user.driver:
        driver_car = Driver_Car.objects.get(email=user.email)
        vehicle = Vehicle.objects.get(plate=driver_car.plate)
    if (request.method == 'POST'):
        edit_profile_form = forms.EditProfileForm(request.POST)
        change_password_form = forms.ChangePasswordForm(request.POST)
        edit_vehicle_form = forms.VehicleForm(request.POST)
        if edit_profile_form.is_valid():
            edit_vehicle_form = forms.VehicleForm(
                initial={'plate': vehicle.plate, 'num_passengers': vehicle.num_passengers, 'vehicle_type': vehicle.vehicle_type})
            email = edit_profile_form.cleaned_data['email']
            firstname = edit_profile_form.cleaned_data['firstname']
            lastname = edit_profile_form.cleaned_data['lastname']
            if email == user.email and firstname == user.firstname and lastname == user.lastname:
                message = 'Nothing changed!'
                return render(request, 'users/edit_profile.html', locals())
            try:
                existed = User.objects.get(email=email)
            except User.DoesNotExist:
                existed = None
            if existed != None and email != user.email:
                message = 'Email already existed!'
                return render(request, 'users/edit_profile.html', locals())
            if user.email != email:
                user.email = email
                driver_car.email = email
                driver_car.save()
                request.session['email'] = user.email
            user.firstname = firstname
            user.lastname = lastname
            user.save()
            message = 'Save successfully'
            return render(request, 'users/edit_profile.html', locals())
        elif change_password_form.is_valid():
            edit_profile_form = forms.EditProfileForm(
                initial={'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname})
            edit_vehicle_form = forms.VehicleForm(
                initial={'plate': vehicle.plate, 'num_passengers': vehicle.num_passengers, 'vehicle_type': vehicle.vehicle_type})
            old_password = change_password_form.cleaned_data['old_password']
            new_password = change_password_form.cleaned_data['new_password']
            new_password2 = change_password_form.cleaned_data['new_password2']
            flag = False
            message = 'Save new password successfully'
            if old_password != user.password:
                message = 'Wrong old password!'
                flag = True
            elif new_password != new_password2:
                message = 'Passwords are not same!'
                flag = True
            elif old_password == new_password:
                message = 'New password is the same to the old one!'
                flag = True
            if flag:
                return render(request, 'users/edit_profile.html', locals())
            user.password = new_password
            user.save()
            return render(request, 'users/edit_profile.html', locals())
        elif edit_vehicle_form.is_valid():
            edit_profile_form = forms.EditProfileForm(
                initial={'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname})
            plate = edit_vehicle_form.cleaned_data['plate']
            vehicle_type = edit_vehicle_form.cleaned_data['vehicle_type']
            num_passengers = edit_vehicle_form.cleaned_data['num_passengers']
            special_vehicle_info = edit_vehicle_form.cleaned_data['special_vehicle_info']
            if plate == vehicle.plate and vehicle_type == vehicle.vehicle_type and num_passengers == vehicle.num_passengers and special_vehicle_info == vehicle.special_vehicle_info:
                message = 'Nothing changed!'
                return render(request, 'users/edit_profile.html', locals())
            try:
                existed = Vehicle.objects.get(plate=plate)
            except Vehicle.DoesNotExist:
                existed = None
            if existed != None and plate != vehicle.plate:
                message = 'Plate already existed!'
                return render(request, 'users/edit_profile.html', locals())
            if plate != vehicle.plate:
                vehicle.plate = plate
                driver_car.plate = plate
                driver_car.save()
            vehicle.num_passengers = num_passengers
            vehicle.vehicle_type = vehicle_type
            vehicle.special_vehicle_info = special_vehicle_info
            vehicle.save()
            message = 'Save successfully'
            return render(request, 'users/edit_profile.html', locals())
        elif not edit_profile_form.is_valid():
            edit_profile_form = forms.EditProfileForm(
                initial={'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname})
            message = "Passenger number should be positive"
            return render(request, 'users/edit_profile.html', locals())
    else:
        edit_profile_form = forms.EditProfileForm(
            initial={'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname})
        change_password_form = forms.ChangePasswordForm(
            initial={'plate': user.email, 'firstname': user.firstname, 'lastname': user.lastname})
        if user.driver:
            edit_vehicle_form = forms.VehicleForm(
                initial={'plate': vehicle.plate, 'num_passengers': vehicle.num_passengers, 'vehicle_type': vehicle.vehicle_type, 'special_vehicle_info': vehicle.special_vehicle_info})
        else:
            edit_vehicle_form = forms.VehicleForm()
    return render(request, 'users/edit_profile.html', {'user': user, 'edit_profile_form': edit_profile_form, 'change_password_form': change_password_form, 'edit_vehicle_form': edit_vehicle_form})


def driver_register(request):
    if 'email' not in request.session:
        return redirect('/login')
    user = User.objects.filter(email=request.session['email']).first()
    email = user.email
    create_date = user.create_date
    if request.method == 'POST':
        register_driver_form = forms.VehicleForm(request.POST)
        if register_driver_form.is_valid():
            plate = register_driver_form.cleaned_data['plate']
            vehicle_type = register_driver_form.cleaned_data['vehicle_type']
            num_passengers = register_driver_form.cleaned_data['num_passengers']

            try:
                existed = Vehicle.objects.get(plate=plate)
            except Vehicle.DoesNotExist:
                existed = None
            if existed != None:
                error_message = 'licence plate existed!'
                return render(request, 'users/driver_register.html', locals())
            vehicle = Vehicle()
            vehicle.plate = plate
            vehicle.vehicle_type = vehicle_type
            vehicle.num_passengers = num_passengers
            vehicle.save()
            driver = Driver_Car()
            driver.email = email
            driver.plate = plate
            driver.save()
            user = User.objects.get(email=email)
            is_driver = True
            user.driver = is_driver
            user.save()
            message = "You are a driver now!"
            return render(request, 'users/profile.html', locals())
        else:
            error_message = "passenger number should be positive"
    else:
        register_driver_form = forms.VehicleForm()
    return render(request, 'users/driver_register.html', locals())


def profile(request):
    if 'email' not in request.session:
        return redirect('/login')
    user = User.objects.get(email=request.session['email'])
    ride_belong_to_as_owner = Ride.objects.filter(
        owner_email=request.session['email']).count()
    try:
        driver_car = get_object_or_404(
            Driver_Car, email=request.session['email'])
        vehicle = get_object_or_404(Vehicle, plate=driver_car.plate)
    except:
        driver_car = None
        vehicle = ''
    # if is_driver:
    return render(request, 'users/profile.html', {'user': user, 'vehicle': vehicle, 'ride_belong_to_as_owner': ride_belong_to_as_owner})


def index(request):
    if 'email' not in request.session:
        return redirect('/login')
    rides_belong_to_ride_id = Ride_Passenger.objects.filter(
        email=request.session['email']).values('ride_id')
    rides_belong_to = Ride.objects.filter(
        ride_id__in=rides_belong_to_ride_id).order_by('status')
    joinable_rides = Ride.objects.exclude(
        Q(ride_id__in=rides_belong_to_ride_id)).filter(status='open')

    user = get_object_or_404(User, email=request.session.get('email'))
    # print(rides_belong_to_ride_id)
    vehicle = None
    confirmed_rides = None
    rides_able_to_claim = None
    if user.driver:
        confirmed_rides = Ride.objects.filter(
            driver=request.session['email'], status='confirmed')
        plate = get_object_or_404(Driver_Car, email=user.email).plate
        vehicle = get_object_or_404(Vehicle, plate=plate)
        max_num_passengers = vehicle.num_passengers
        vehicle_type = vehicle.vehicle_type
        special_vehicle_info = vehicle.special_vehicle_info
        rides_able_to_claim = Ride.objects.filter(Q(vehicle_type="") | Q(vehicle_type=vehicle_type)).filter(
            num_passengers__lte=max_num_passengers, status='open').filter(
                Q(special_request="") | Q(special_request=special_vehicle_info)).exclude(Q(owner_email=request.session['email']) | Q(ride_id__in=rides_belong_to_ride_id))

    return render(request, 'users/index.html', {'confirmed_rides': confirmed_rides, 'joinable_rides': joinable_rides, 'rides_belong_to': rides_belong_to, 'vehicle': vehicle, 'rides_able_to_claim': rides_able_to_claim})


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if not user:
                error_message = 'user does not exist'
                return render(request, 'users/login.html', locals())
            else:
                if user.password == password:
                    request.session['email'] = user.email
                    request.session.set_expiry(0)
                    return redirect('/index')
                else:
                    error_message = 'wrong email or password'
                    return render(request, 'users/login.html', locals())
    else:
        login_form = forms.LoginForm()
    return render(request, 'users/login.html', locals())


@transaction.atomic
def register(request):
    # if 'email' in request.session:
    #     return redirect('/index')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            password = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            firstname = register_form.cleaned_data['firstname']
            lastname = register_form.cleaned_data['lastname']
            try:
                existed = User.objects.get(email=email)
            except:
                existed = None
            if existed is not None:
                error_message = 'email existed!'
                return render(request, 'users/register.html', locals())
            if password != password2:
                error_message = 'passwords are not same!'
                return render(request, 'users/register.html', locals())
            current_user = User()
            current_user.email = email
            current_user.password = password
            current_user.password2 = password2
            current_user.firstname = firstname
            current_user.lastname = lastname
            current_user.save()
            return redirect('/login')
    else:
        register_form = forms.RegisterForm()
    return render(request, 'users/register.html', locals())


def logout(request):
    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect('/login')


def ride_request(request):
    if 'email' not in request.session:
        return redirect('/index')
    if request.method == 'POST':
        ride_request_form = forms.RideRequestForm(request.POST)
        if ride_request_form.is_valid():
            dest_addr = ride_request_form.cleaned_data['dest_addr']
            arrival_time = ride_request_form.cleaned_data['arrival_time']
            sharable = ride_request_form.cleaned_data['sharable']
            num_passengers = ride_request_form.cleaned_data['num_passengers']
            vehicle_type = ride_request_form.cleaned_data[
                'vehicle_type'] if 'vehicle_type' in ride_request_form.cleaned_data else None
            special_request = ride_request_form.cleaned_data['special_request']
            ride = Ride()
            ride.owner_email = request.session['email']
            ride.dest_addr = dest_addr
            ride.arrival_time = arrival_time
            ride.sharable = True if sharable == 'yes' else False
            ride.vehicle_type = vehicle_type if vehicle_type != None else ''
            ride.ride_id = uuid.uuid1()
            ride.num_passengers = num_passengers
            ride.owner_num_passengers = num_passengers
            ride.special_request = special_request
            ride.save()
            ride_passenger = Ride_Passenger()
            ride_passenger.ride_id = ride.ride_id
            ride_passenger.email = ride.owner_email
            ride_passenger.party_num_passengers = num_passengers
            ride_passenger.role = 'owner'
            ride_passenger.save()
            message = 'success'
        else:
            message = 'Passenger number must be positive!'
            return render(request, 'users/ride_request.html', locals())
        return redirect('users:index')
    else:
        ride_request_form = forms.RideRequestForm()
    return render(request, 'users/ride_request.html', locals())


def ride_detail(request, slug):
    if 'email' not in request.session:
        return redirect('/index')
    ride = get_object_or_404(Ride, ride_id=slug)
    message = ""
    # get old owner_num_passengers of the ride
    old_owner_num_passengers = ride.owner_num_passengers
    # get sharable status
    sharable = ride.sharable
    # get old dest_addr, arrival_time
    old_arrival_time = ride.arrival_time
    # get party number based on the role of user
    old_dest_addr = ride.dest_addr
    old_special_request = ride.special_request
    joined = True
    if request.session['email'] == ride.owner_email:
        party_number = ride.owner_num_passengers
    else:
        try:
            party_number = get_object_or_404(
                Ride_Passenger, ride_id=ride.ride_id, email=request.session['email']).party_num_passengers
        except:
            party_number = 0
            joined = False
    # get shares of this ride
    if request.method == 'POST':
        ride_detail_form = forms.RideDetailForm(request.POST, instance=ride)
        if 'save_change' in request.POST:
            if ride_detail_form.is_valid():
                ride_detail_form.save(commit=False)
                # get data from the form
                dest_addr = ride_detail_form.cleaned_data['dest_addr']
                arrival_time = ride_detail_form.cleaned_data['arrival_time']
                owner_num_passengers = ride_detail_form.cleaned_data['owner_num_passengers']
                special_request = ride_detail_form.cleaned_data['special_request']
                # if the party number has changed, we update the whole num_pasengers
                # and we update the ride_passenger table
                if party_number != owner_num_passengers:
                    ride.num_passengers += (owner_num_passengers -
                                            party_number)
                    ride_passenger = get_object_or_404(
                        Ride_Passenger, ride_id=slug, email=request.session['email'])
                    ride_passenger.party_num_passengers = owner_num_passengers
                    ride_passenger.save()

                # if the role is the owner
                if request.session['email'] == ride.owner_email:
                    if dest_addr == old_dest_addr and arrival_time == old_arrival_time and owner_num_passengers == old_owner_num_passengers and special_request == old_special_request:
                        message = 'Nothing changed!'
                        return render(request, 'users/ride_detail.html', locals())
                    else:  # make changes, need to cancle ride for share
                        # notify the share of cancling their ride
                        ride.num_passengers = owner_num_passengers
                        send_mail_cancle(slug)
                        # delete corresponding data in ride_passenger table
                        Ride_Passenger.objects.filter(
                            ride_id=slug, role='sharer').delete()
                    print(owner_num_passengers, ride.owner_num_passengers)
                    ride.owner_num_passengers = owner_num_passengers
                else:
                    ride.owner_num_passengers = old_owner_num_passengers
                # ride.arrival_time = old_arrival_time if dest_addr ==
                #ride.arrival_time = old_arrival_time
                ride.sharable = sharable
                ride.special_request = special_request
                ride.save()
                print(ride.owner_num_passengers)
                message = 'save change successfully!'
                # update the data in the front end
                party_number = owner_num_passengers
            else:
                message = "Passenger number must be positive!"
        elif "cancel_order" in request.POST:
            # TODO: notify sharers and remove them
            # owner leave, remove records
            if ride.owner_email == request.session['email']:
                send_mail_cancle(slug)
                Ride_Passenger.objects.filter(ride_id=slug).delete()
                ride.delete()
            else:
                ride_passenger = Ride_Passenger.objects.get(
                    email=request.session['email'], ride_id=slug)
                ride.num_passengers -= ride_passenger.party_num_passengers
                ride.save()
                ride_passenger.delete()
            return redirect('users:index')
        elif "join" in request.POST:
            joined = True
            if ride_detail_form.is_valid():
                ride_detail_form.save(commit=False)
                # get data from the form
                owner_num_passengers = ride_detail_form.cleaned_data['owner_num_passengers']

                if owner_num_passengers <= 0:
                    message = "passenger number has to be bigger than 0"
                    joined = False
                    ride.arrival_time = old_arrival_time
                    ride.sharable = sharable
                else:
                    ride.num_passengers += owner_num_passengers
                    ride_passenger = Ride_Passenger()
                    ride_passenger.ride_id = slug
                    ride_passenger.email = request.session['email']
                    ride_passenger.role = 'sharer'
                    ride_passenger.party_num_passengers = owner_num_passengers
                    ride_passenger.save()

                    # ride.arrival_time = old_arrival_time if dest_addr ==
                    ride.arrival_time = old_arrival_time
                    ride.sharable = sharable
                    ride.owner_num_passengers = old_owner_num_passengers
                    ride.save()
                    message = 'join successfully!'
                    # update the data in the front end
                party_number = owner_num_passengers
        elif "complete" in request.POST:
            ride.status = "complete"
            ride.save()

    sharers = Ride_Passenger.objects.filter(
        ride_id=ride.ride_id).exclude(email=ride.owner_email) if ride.sharable else None
    ride_detail_form = forms.RideDetailForm(
        initial={'ride_id': ride.ride_id, 'owner_email': ride.owner_email, 'dest_addr': ride.dest_addr, 'arrival_time': ride.arrival_time,
                 'ride_plate': ride.ride_plate, 'sharable': ride.sharable, 'status': ride.status, 'create_date': ride.create_date,
                 'num_passengers': ride.num_passengers, 'owner_num_passengers': party_number, 'driver': ride.driver, 'vehicle_type': ride.vehicle_type,
                 'special_request': ride.special_request})
    return render(request, 'users/ride_detail.html', {'ride': ride, 'ride_detail_form': ride_detail_form, 'message': message, 'sharers': sharers, 'joined': joined})


def confirm_ride_detail(request, slug):
    if 'email' not in request.session:
        return redirect('/index')

    ride = get_object_or_404(Ride, ride_id=slug)
    if request.method == 'POST':
        if 'complete' in request.POST:
            ride.status = "complete"
            ride.save()
    elif request.method == 'GET':
        if ride.status == 'open':
            send_mail(slug)
        ride = get_object_or_404(Ride, ride_id=slug)
        ride.status = "confirmed"
        ride.driver = request.session['email']
        driver_car = get_object_or_404(
            Driver_Car, email=request.session['email'])
        vehicle = get_object_or_404(Vehicle, plate=driver_car.plate)
        ride.vehicle_type = vehicle.vehicle_type
        ride.ride_plate = driver_car.plate
        ride.save()

    sharers = Ride_Passenger.objects.filter(
        ride_id=ride.ride_id).exclude(email=ride.owner_email) if ride.sharable else None
    ride_detail_form = forms.RideDetailForm(
        initial={'ride_id': ride.ride_id, 'owner_email': ride.owner_email, 'dest_addr': ride.dest_addr, 'arrival_time': ride.arrival_time,
                 'ride_plate': ride.ride_plate, 'sharable': ride.sharable, 'status': ride.status, 'create_date': ride.create_date,
                 'num_passengers': ride.num_passengers, 'owner_num_passengers': ride.num_passengers, 'driver': ride.driver, 'vehicle_type': ride.vehicle_type,
                 'special_request': ride.special_request})
    return render(request, 'users/confirm_ride_detail.html', {'ride': ride, 'ride_detail_form': ride_detail_form, 'sharers': sharers})


def send_mail(ride_id):
    email_list = [i[0] for i in Ride_Passenger.objects.filter(
        ride_id=ride_id).values_list('email')]
    subject = 'Your ride[] has been confirmed!'
    text_content = 'Your ride has been confirmed! Please go to the pick-up loaction on time.'
    html_content = '''
    <p>Woo hoo! Your ride has been confirmed. Please go to the pick-up loaction on time.</p >
    <p>Have a nice ride!</p >
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    # to = 'cyprinoid_b@163.com'  # to = '', '', ''   可接多个邮箱地址
    msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse({'status': '邮件已经发送成功！'})


def send_mail_cancle(ride_id):
    email_list = [i[0] for i in Ride_Passenger.objects.filter(
        ride_id=ride_id, role='sharer').values_list('email')]
    subject = 'Your ride has been cancled!'
    text_content = 'Your ride has been cancled!'
    html_content = '''
    <p>What a pity! Your ride has been cancled.</p >
    <p>Please go back and look for another ride.</p >
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    # to = 'cyprinoid_b@163.com'  # to = '', '', ''   可接多个邮箱地址
    msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse({'status': '邮件已经发送成功！'})
