from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
import bcrypt

def index(request):
    return render(request,'index.html')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/dashboard/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(request, 'That email is not in our system, please register for an account')
    return redirect('/')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if len (errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/')

def dashboard(request):
    return render(request,'dashboard.html')

def new(request):
    return render(request,'new.html')