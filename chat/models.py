from turtle import update
from django.db import models
from accounts.models import User
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    room_name = models.ForeignKey(
        Room, related_name="message", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message
