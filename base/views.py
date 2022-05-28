from mimetypes import init
from urllib import response
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm


# Dummy data
# rooms = [
#     {'id':1, 'name':'lets learn python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'}
#     ]
# Create your views here.
def home(request):
    # We can create a variable to pass our dictionary in as a variable
    # We can pull objects from the db
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # print(room)
    context = {'room':room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
# Instantiate a Room 

    if request.method == 'POST':
        form = RoomForm(request.POST)
        # We add the data to the form with request.POST, django already knows what information to extract from the input from our RoomForm
        if form.is_valid():
        # We use the is_valid() method to check the input data
            form.save()
        # If it is valid, we use the save() method to save the model in the database
            return redirect('home')
        # Now we'll redirect our user, using the redirect() method, back to the 'home' page. We can utilize the path name, from urls.py
    
    context = { 'form': form }
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

