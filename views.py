from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "login_reg_app/index.html")

def register(request):
    errors = User.objects.validator(request.POST)

    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    
    else:
        messages.success(request, "Successfully created new user!")
        
        first_name    = request.POST['first_name']
        last_name     = request.POST['last_name']
        email_address = request.POST['email_address']
        password      = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(password)
        User.objects.create(first_name=first_name, last_name=last_name, email_address=email_address, password=password)
    return redirect('/show')

def login(request):
    try:
        user = User.objects.get(email_address=request.POST['email_address'])
    except:
        messages.error(request, "Email address not found in database")
        print("EMAIL NOT FOUND???")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.success(request, "Successfully logged in")
    else:
        messages.error(request, "Wrong password")
    return redirect('/')

def show(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, "login_reg_app/show.html", context)
