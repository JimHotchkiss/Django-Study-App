# Import HttpResponse
import re
from django.http import HttpResponse
from django.db.models import Q 
from django.shortcuts import render, redirect
# Import User for our login 
from django.contrib.auth.models import User
# Import UserCreation Form
from django.contrib.auth.forms import UserCreationForm
# Import authenticate, login and logout
from django.contrib.auth import authenticate, login, logout 
# Import login_required 
from django.contrib.auth.decorators import login_required
# Import our flash message 
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm

# User login 
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # We want to check if the user exist
        try:
            user = User.objects.get(username=username)
        except:
        # If does not exist, we want to show the user a flash message
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)
# Logout 
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
    return render(request, 'base/login_register.html', {'form': form })

def home(request):
    # We can create a variable to pass our dictionary in as a variable
    # We can pull objects from the db
    # We'll grab the parameter defined in q and filter our rooms with this parameter
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Instead of grabbing all rooms, we'll filter through q. Note: this may include 'All' topics
    # rooms = Room.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    # Use the Q object to filter room_messages
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    # print(room)
    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


# Create UserProfile
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
# Instantiate a Room 

    if request.method == 'POST':
        form = RoomForm(request.POST)
        # We add the data to the form with request.POST, django already knows what information to extract from the input from our RoomForm
        if form.is_valid():
        # We use the is_valid() method to check the input data
            room = form.save(commit=False)
            room.host = request.user
            room.save()
        # If it is valid, we use the save() method to save the model in the database
            return redirect('home')
        # Now we'll redirect our user, using the redirect() method, back to the 'home' page. We can utilize the path name, from urls.py
    
    context = { 'form': form }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not authorized to update room')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not authorized to delete room') 

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not authorized to delete message') 

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})