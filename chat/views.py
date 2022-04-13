from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import Message
# Create your views here.


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class RoomView(LoginRequiredMixin, View):
    def get(self, request, room_name, *args, **kwargs):
        messages = Message.objects.filter(room_name__name=room_name)
        context = {
            'room_name': room_name,
            'messages': messages,
        }
        return render(request, 'chat/room.html', context)
