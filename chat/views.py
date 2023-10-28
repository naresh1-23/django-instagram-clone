from django.shortcuts import render, redirect
from user.models import Profile, User
from .models import Room, Chat
from django.db.models import Q


# Create your views here.
def chat(request):
    user = request.user
    rooms = Room.objects.filter(Q(user1 = user) | Q(user2 = user))
    rooms_arr = []
    for single_room in rooms:
        chat = Chat.objects.filter(room = single_room).order_by("-id")
        if single_room.user1 == user:
            dedicated_user = single_room.user2
        else:
            dedicated_user = single_room.user1
        msg_profile = Profile.objects.filter(user = dedicated_user).first()
        value_dict = {}
        if chat:
            value_dict["id"] = dedicated_user.id
            value_dict["username"] = dedicated_user.username
            value_dict["profile_img"] = msg_profile.profile_img.url
            value_dict["last_message"] = chat[0].message
            rooms_arr.append(value_dict)
    profile = Profile.objects.filter(user = user).first()
    return render(request, "chat/chat.html", {"user": user, "profile": profile, "rooms_arr": rooms_arr})

def chat_room(request, pk):
    room = Room.objects.filter(id = pk).first()
    user = request.user
    if room.user1 == user:
        another_user = room.user2
    else:
        another_user = room.user1
    another_profile = Profile.objects.filter(user = another_user).first()
    rooms = Room.objects.filter(Q(user1 = user) | Q(user2 = user))
    rooms_arr = []
    for single_room in rooms:
        chat = Chat.objects.filter(room = single_room).order_by("-id")
        if single_room.user1 == user:
            dedicated_user = single_room.user2
        else:
            dedicated_user = single_room.user1
        msg_profile = Profile.objects.filter(user = dedicated_user).first()
        value_dict = {}
        if chat:
            value_dict["id"] = dedicated_user.id
            value_dict["username"] = dedicated_user.username
            value_dict["profile_img"] = msg_profile.profile_img.url
            value_dict["last_message"] = chat[0].message
            rooms_arr.append(value_dict)
    print(rooms_arr)
    chats = Chat.objects.filter(room = room)
    profile = Profile.objects.filter(user = user).first()
    return render(request, "chat/chat_room.html", {"user": user, "profile": profile, "chats": chats, "rooms_arr": rooms_arr, "another_user": another_user, "another_profile": another_profile, "room": room})

def check_room(request, pk):
    another = User.objects.filter(id = pk).first()
    user = request.user
    room = Room.objects.filter(Q(user1 = another, user2 = user) | Q(user1 = user, user2 = another)).first()
    if room:
        return redirect("chat-room", pk = room.id)
    else:
        room1 = Room.objects.create(user1 = another, user2 = user)
        room1.save()
        return redirect("chat-room", pk = room1.id)
    