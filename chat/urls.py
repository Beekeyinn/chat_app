from unicodedata import name
from django.urls import path

from chat.views import RoomView

urlpatterns = [
    path('<str:room_name>/', RoomView.as_view(), name="room"),
]
