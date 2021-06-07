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
            return redirect('/dashboard')
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
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'movies': Movie.objects.all()
    }
    return render(request,'dashboard.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')


def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request,'newMovie.html')

def create(request):
    #run for errors before creating a show
    errors = Movie.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/new')
    #create a movie
    Movie.objects.create(
        title = request.POST['title'],
        network = request.POST['network'],
        release_date = request.POST['release_date'],
        description = request.POST['description']
    )
    return redirect('/dashboard')

def edit(request, movie_id):
    one_movie = Movie.objects.get(id=movie_id)
    context = {
        'movie': one_movie
    }
    return render(request, 'editMovie.html',context)

def update(request, movie_id):
    errors = Movie.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/dashboard/{movie_id}/edit')
    # updates movie
    to_update = Movie.objects.get(id=movie_id)
    # updates each field
    to_update.title = request.POST['title']
    to_update.release_date = request.POST['release_date']
    to_update.network = request.POST['network']
    to_update.description = request.POST['description']
    print("to update", to_update)
    to_update.save()
    return redirect(f'/dashboard/{movie_id}')

def movie(request, movie_id):
    one_movie = Movie.objects.get(id=movie_id)
    context = {
        'movie': one_movie,
    }
    return render(request, 'movie.html',context)

def delete(request, movie_id):
    to_delete = Movie.objects.get(id=movie_id)
    to_delete.delete()
    return redirect('/dashboard')

def add_like(request, movie_id):
    liked_movie= Movie.objects.get(id=movie_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_movie.user_likes.add(user_liking)
    return redirect(f'/dashboard/{movie_id}')
