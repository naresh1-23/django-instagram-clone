from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, Profile, ConfirmationCode, Follow
from django.contrib.auth import login as auth_login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from random import randint

def sendVerifyEmail(email, user):
    subject = "Email Verification"
    otp = randint(10000,99999)   
    message = f"Your verification code is {otp}."
    otpModel = ConfirmationCode.objects.create(code = otp, user = user)
    otpModel.save()
    from_email =  settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        fullname = request.POST['fullname']
        password = request.POST['password']
        if email == '' or username == '' or fullname == '' or password == '':
            messages.warning(request, "Fields cannot be empty")
            return redirect('signup')
        user = User.objects.filter(username = username).first()
        if user:
            messages.warning(request, "User already exists")
            return redirect('signup')
        else:
            hashed_pass = make_password(password)
            user2 = User.objects.filter(email = email).first()
            if user2:
                messages.warning(request, "User already exists")
                return redirect('signup')
            user1 = User.objects.create(email = email, username = username, fullname = fullname, password = hashed_pass)
            user1.save()
            profile = Profile.objects.create(user = user1)
            profile.save()
            auth_login(request, user1)
            sendVerifyEmail(request.user.email, user1)
            return redirect('confirmation-code')
    return render(request, "user/signup.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("profile", pk = request.user.id)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = make_password(password)
        print(hashed_password)
        user = User.objects.filter(email = email).first()
        if user:
            if authenticate(request, username = user.username, password = password):   
                auth_login(request, user)
                messages.success(request, "logged in successfully")
                return redirect("profile", pk = user.id)
            messages.warning(request, "User doesn't exist")
            return redirect('login')
        else:
            messages.warning(request, "User doesn't exist")
            return redirect('login')
    return render(request, "user/login.html")


def confirmation_code(request):
    if request.method == "POST":
        code = request.POST['confirmation_code']
        if code == "":
            messages.warning(request, "Fields cannot be empty")
            return redirect("confirmation-code")
        else:
            otp = ConfirmationCode.objects.filter(user = request.user, code = code).first()
            if otp:
                messages.success(request, "Successfully verified")
                user = request.user
                user.is_verified = True
                user.save()
                otp.delete()
                return redirect("profile", pk=1)
            messages.warning(request, "Invalid code")
            return redirect("confirmation-code")            
    return render(request, "user/confirmation_code.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")


def follow(request, pk):
    user_follow = User.objects.filter(id = pk).first()
    follow = Follow.objects.filter(followed_to=user_follow, followed_by=request.user).first()
    if follow:
        messages.warning(request, f"already followed")
    else:
        follow_model = Follow.objects.create(followed_to= user_follow, followed_by=request.user)
        follow_model.save()
        return redirect("profile", pk = pk)
    