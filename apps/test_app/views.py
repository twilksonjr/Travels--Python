from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import *
import bcrypt
from datetime import datetime

def Index(request):
    return render(request,"test_app/index.html")

def Registration(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        registeredUser = Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1)
        request.session["user_id"] = registeredUser.id
        return redirect('/dashboard')

def Login(request):
    errors = Users.objects.login_validator(request.POST)
    if not len(errors):
        user = Users.objects.get(email = request.POST['login_email'])
        request.session["user_id"] = user.id
        return redirect("/dashboard")
    # if the login information is NOT correct
    else:
        print("*"*80)
        print('validation failed on login')
        print("*"*80)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

# Render Route
def Dashboard(request):   
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "logged_in_user" : Users.objects.get(id=request.session["user_id"]),
        "all_trips" : Trips.objects.all()
    }
    return render(request,"test_app/dashboard.html", context)

# Render Route
def Trip(request):
    context = {

        "logged_in_user" : Users.objects.get(id=request.session["user_id"]),
    }
    return render(request,"test_app/trip.html", context)

# Render route
def Edit_trip(request, trip_id):
    

    this_trip_object = Trips.objects.get(id= trip_id)
    this_destination = this_trip_object.destination
    this_start_date = this_trip_object.start_date
    this_end_date = this_trip_object.end_date
    this_plan = this_trip_object.plan

    context = {
        "logged_in_user" : Users.objects.get(id=request.session["user_id"]),
        'this_trip': this_trip_object,
        'destination':this_destination,
        'start_date':this_start_date,
        'end_date':this_end_date,
        'plan':this_plan,
    }
    return render(request,"test_app/edit_trip.html",context)

# Process route
def Update_trip(request, trip_id):
    errors = Trips.objects.validate_event(request.POST)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_trip/{trip_id}')
    temp = Trips.objects.get(id = trip_id)
    temp.destination = request.POST["destination"]
    temp.start_date = request.POST["start_date"]
    temp.end_date = request.POST["end_date"]
    temp.plan = request.POST["plan"]
    temp.save()
    return redirect('/dashboard')


# Process Route
def Create_trip(request):
    errors = Trips.objects.validate_event(request.POST)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trip')

    
    # user = Users.objects.get(id=user_id)
    # created_by_id = request.session["user_id"]
    # print(f"This is request.session {request.session.user_id}")
    user = Users.objects.get(id=request.session["user_id"])
    destination = request.POST["destination"]
    start_date = request.POST['start_date']
    end_date = request.POST["end_date"]
    plan = request.POST["plan"]
    Trips.objects.create(
        destination=destination, 
        start_date=start_date, 
        end_date=end_date,
        plan=plan,
        created_by=user
        )
    return redirect('/dashboard')

def Read(request, trip_id):
    this_trip_object = Trips.objects.get(id= trip_id)
    this_destination = this_trip_object.destination
    this_start_date = this_trip_object.start_date
    this_end_date = this_trip_object.end_date
    this_plan = this_trip_object.plan

    context = {
        "logged_in_user" : Users.objects.get(id=request.session["user_id"]),
        'this_trip': this_trip_object,
        'destination':this_destination,
        'start_date':this_start_date,
        'end_date':this_end_date,
        'plan':this_plan,
    }
    return render(request,"test_app/read.html", context)


def Logout(request):
    if 'user_id' not in request.session:
        # logged_in_user = (Users.objects.get(id=request.session["user_id"])
        return('/')
    else:
        del request.session['user_id']
        request.session.clear()
        return redirect('/')

def Delete_trip(request, trip_id):
    # query the movie whose page we're on using the url
    this_trip_object = Trips.objects.get(id= trip_id)
    # delete the logged in user object from the list of attendees (reference the platform on the ManyToMany tab)
    this_trip_object.delete()

    return redirect ('/dashboard')

