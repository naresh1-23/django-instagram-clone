from django.shortcuts import render, redirect
from user.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def profile(request, pk):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.filter(user = user).first()
        range =  [1,2,3,4,5,6,7,8,9,10]
        return render(request, "post/profile.html", {"user": user, "profile": profile, "range": range})
    messages.warning(request, "Please login")
    return redirect('login')

def single_post(request, pk):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.filter(user = user).first()
        range = [1,2,3,4,5,6,7,8,9]
        return render(request, "post/singlepost.html", {"user": user, "profile": profile, "range": range})
    messages.warning(request, "Please login")
    return redirect('login')