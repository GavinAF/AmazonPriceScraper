from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create views here.

@login_required(login_url="/")
def dashboard(response):

    if response.user.is_authenticated:
        username = response.user.username

    return render(response, "dashboard/dashboard.html", {"username":username})