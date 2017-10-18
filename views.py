from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    if checkLogin(request):
        return redirect('/show')
    return render(request, "login_reg_app/index.html")

def register(request):
    logout(request)
    errors = User.objects.validator(request.POST, 'create')

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

        # Create new user
        user = User.objects.create(first_name=first_name, last_name=last_name, email_address=email_address, password=password)

        request.session['id'] = user.id
        request.session['email'] = user.email_address
        request.session['name'] = user.first_name

    return redirect('/show')

def login(request):
    logout(request)
    try:
        user = User.objects.get(email_address=request.POST['email_address'])
    except:
        messages.error(request, "Email address not found in database")
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.success(request, "Successfully logged in")

        # Add user details to session
        request.session['id'] = user.id
        request.session['email'] = user.email_address
        request.session['name'] = user.first_name

        return redirect('/show')
    else:
        messages.error(request, "Wrong password")
    return redirect('/')

def show(request):
    context = {
        'users': User.objects.all(),
        'loggedIn': checkLogin(request),
    }
    return render(request, "login_reg_app/show.html", context)

def destroy(request, id):
    if checkLogin(request):
        if request.session['id'] == int(id):
            User.objects.get(id=id).delete()
    else:
        messages.error(request, "Must be logged in to do that")
    return redirect('/')

def edit(request, id):
    if checkLogin(request):
        if request.session['id'] == int(id):
            context = {
                'user': User.objects.get(id=id)
            }
            return render(request, 'login_reg_app/edit.html', context)
    else:
        messages.error(request, "Must be logged in to do that")
        return redirect('/')

def show_one(request, id):
    context = {
        'user': User.objects.get(id=id),
        'loggedIn': checkLogin(request),
    }
    return render(request, 'login_reg_app/show_one.html', context)

def update(request, id):
    if request.POST:
        errors = User.objects.validator(request.POST, 'update')

        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/edit/' + id)

        first_name     = request.POST['first_name']
        last_name      = request.POST['last_name']
        email_address  = request.POST['email_address']
        currPassword   = request.POST['password_current']
        newPassword    = request.POST['password_new']
        confPassword   = request.POST['password_confirm']

        # Check if password fields are empty
        updatePassword = len(currPassword) + len(newPassword) + len(confPassword) > 1

        try:
            user =  User.objects.get(id=id)
        except:
            messages.error(request, "User not in database")
            return redirect('/')

        if updatePassword:
            oldPassword  = user.password.encode()
            currPassword = currPassword.encode()
            if bcrypt.checkpw(currPassword, oldPassword):
                newPassword = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())
                user.password = newPassword
                user.save()
            else:
                messages.error(request, "Wrong current password")
                return redirect('/edit/' + id)

        user.first_name    = first_name
        user.last_name     = last_name
        user.email_address = email_address
        user.save()
        messages.success(request, "User successfully updated")

        return redirect('/show/' + id)
    else:
        messages.error(request, "Must be logged in to do that")
        return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

def checkLogin(request):
    return 'id' in request.session

def logout(request):
    request.session.flush()
