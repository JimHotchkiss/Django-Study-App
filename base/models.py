from enum import auto
from operator import mod
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# A Topic can have many Rooms 
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
# Room has-one Topic
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # We can create a class that customizes the oder of the rooms, the most recently created rooms appearing first. ['updated', 'created'] will render them in ascending order, if you put the - infront of each descripter, it will invert that order, or making it descending
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


# One-to-many relationship: A room has many messages
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]