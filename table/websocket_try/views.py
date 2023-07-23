from django.shortcuts import render

def index(request):
    return render(request, "socket/websocket.html")

def room(request, room_name):
    return render(request, "socket/room.html", {"room_name": room_name})