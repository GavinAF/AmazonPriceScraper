from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(response):

    if response.user.is_authenticated:
        return redirect("dashboard:dashboard")

    # Get data from POST
    if response.method == 'POST':
        if 'register' in response.POST:
            username = response.POST.get("username", "")
            email = response.POST.get("email", "")
            password = response.POST.get("password", "")

            # Create new user with inputted data
            new_user = User.objects.create_user(username, email, password)
            new_user.save()

            user = authenticate(response, username=username, password=password)
            if user is not None:
                login(response, user)
                return redirect("dashboard:dashboard")

    return render(response, "main/home.html")

def login_view(response):

    if response.method == "POST":
        if "login" in response.POST:
            username = response.POST.get("username", "")
            password = response.POST.get("password", "")

            user = authenticate(response, username=username, password=password)
            if user is not None:
                login(response, user)
                return redirect("dashboard:dashboard")


    return render(response, "main/login.html")

def register_view(response):
    return render(response, "main/register.html")

@login_required(login_url="/")
def logout_view(response):
    logout(response)
    return redirect("main:home")