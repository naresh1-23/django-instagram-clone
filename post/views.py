from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import User, Profile, Follow
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
import random
from django.core import serializers
import json


def profile(request, pk):
    if request.user.is_authenticated:
        user = request.user
        user_data = User.objects.filter(id = pk).first()
        follow = Follow.objects.filter(followed_by=user, followed_to=user_data).first()
        follower = Follow.objects.filter(followed_to=user_data).count()
        following = Follow.objects.filter(followed_by = user_data).count()
        profile = Profile.objects.filter(user = user).first()
        profile_data = Profile.objects.filter(user = user_data).first()
        posts = Post.objects.filter(user = user_data)
        post_number = posts.count()
        return render(request, "post/profile.html", {"user": user, "profile": profile, "posts": posts, "user_data": user_data, "profile_data": profile_data, "follow": follow, "following": following, "follower": follower, "post_number": post_number})
    messages.warning(request, "Please login")
    return redirect('login')

def single_post(request, pk):
    if request.user.is_authenticated:
        user = request.user
        logged_profile = Profile.objects.filter(user = user).first()
        post = Post.objects.filter(id = pk).first()
        profile = Profile.objects.filter(user = post.user).first()
        range = [1,2,3,4,5,6,7,8,9]
        return render(request, "post/singlepost.html", {"user": user, "profile": profile, "post": post, "range": range, "logged_profile": logged_profile})
    messages.warning(request, "Please login")
    return redirect('login')

def add_post(request):
    user = request.user
    profile = Profile.objects.filter(user = user).first()
    if request.method == "POST":
        image = request.FILES['image_path']
        caption = request.POST['caption']
        if image == "":
            messages.warning(request, f"Image Field cannot be empty")
            return redirect("add-post")
        post = Post.objects.create(caption = caption, post_image = image, user = user, profile = profile)
        post.save()
        messages.success(request, f"post successfully uploaded")
        return redirect("profile" , pk = user.id)
    return render(request, "post/addpost.html", {"user": user, "profile": profile})


def home(request):
    user = request.user
    profile = Profile.objects.filter(user = user).first()
    followed = Follow.objects.filter(followed_by=user)
    posts = []
    for follow in followed:
        posted = Post.objects.filter(user = follow.followed_to)
        for poster in posted:
            new = {}
            new["id"] = poster.id
            new["caption"] = poster.caption
            new["post_image"] = poster.post_image.url
            new["user"] = poster.user
            new["profile"] = poster.profile
            new["posted_date"] = poster.posted_date
            posts.append(new)         
    random.shuffle(posts)
    return render(request, "post/mainapge.html", {"posts": posts, "user": user, "profile": profile})

def search(request):
    user = request.user
    profile = Profile.objects.filter(user= user).first()
    return render(request, "post/search.html", {"user": user, "profile": profile})

def search_data(request, data):
    search_data = User.objects.filter(username__icontains = data)
    profile = []
    for data in search_data:
        user_profile = Profile.objects.filter(user = data).first()
        new = {}
        new["id"] = data.id
        new["profile_img"]= user_profile.profile_img.url
        new["username"] = data.username
        new["fullname"] = data.fullname
        profile.append(new)
    res_data = json.dumps(profile)
    return HttpResponse(res_data,content_type="application/json")