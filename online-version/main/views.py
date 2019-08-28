from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

# Create your views here.

def home(response):
    if response.method == 'POST':
        if 'register' in response.POST:
            register_form = RegisterForm(response.POST, prefix='register')
            if register_form.is_valid():
                register_form.save()
            login_form = AuthenticationForm(prefix='login')

        elif 'login' in response.POST:
            login_form = AuthenticationForm(data=response.POST, prefix='login')
            if login_form.is_valid():
                login_form.save() 
                # login the user

                return redirect("dashboard/")
            register_form = RegisterForm(prefix='register')

    else:
        register_form = RegisterForm(prefix='register')
        login_form = AuthenticationForm(prefix='login')
    
    return render(response, "main/home.html", {"login_form":login_form, "register_form":register_form})


#def home(response):
 #   if response.method == "POST":
  #      form = RegisterForm(response.POST)
   #     if form.is_valid():
    #        form.save()
    #else:
     #   form = RegisterForm()

    #return render(response, "main/home.html", {"form":form})
