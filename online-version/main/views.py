from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(response):

    if response.user.is_authenticated:
        return redirect("dashboard:dashboard")

    if response.method == 'POST':
        if 'register' in response.POST:
            register_form = RegisterForm(response.POST, prefix='register')
            if register_form.is_valid():
                register_form.save()
            login_form = LoginForm(prefix='login')

        elif 'login' in response.POST:
            login_form = LoginForm(data=response.POST, prefix='login')
            if login_form.is_valid():

                user = login_form.get_user()
                login(response, user)

                return redirect("dashboard/")
            register_form = RegisterForm(prefix='register')

    else:
        register_form = RegisterForm(prefix='register')
        login_form = LoginForm(prefix='login')
    
    return render(response, "main/home.html", {"login_form":login_form, "register_form":register_form})
    
@login_required(login_url="/")
def logout_view(response):
    if response.method == "POST":
        logout(response)
        return redirect("main:home")