from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm

# Create your views here.

def home(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    return render(response, "main/home.html", {"form":form})
