from urllib import response
from django.shortcuts import render
from .models import Room


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

    context = {}
    return render(request, 'base/room_form.html', context)
