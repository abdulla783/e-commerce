from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['signupemail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Check for error inputs
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 character')
            return redirect('/shop')

        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('/shop')

        if pass1 != pass2:
            messages.error(request, 'Password do not match ')
            return redirect('/shop')

        if len(pass1) and len(pass2) <= 4:
            messages.error(request, 'Length of passwords must be greater than 4')
            return redirect('/shop')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username has already taken. Please try another one!')
            return redirect('/shop')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email has already taken. Please try another one!')
            return redirect('/shop')

        # Creating User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your Saim Cart account has been successfully created!')
        return redirect('/shop')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('/shop')
        else:
            messages.error(request, 'Invalid Username or Password try again!')
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/shop')