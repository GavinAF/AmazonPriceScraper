from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Link

# Create views here.

@login_required(login_url="/")
def dashboard(response):

    if response.user.is_authenticated:
        user = response.user
        username = response.user.username

    link_count = Link.objects.all().filter(owner=user).count()

    return render(response, "dashboard/dashboard.html", {"username":username, "link_count":link_count})

@login_required(login_url="/")
def profile(response):
    return render(response, "dashboard/user.html", {})

@login_required(login_url="/")
def view_links(response):

    if response.user.is_authenticated:
        user = response.user
        username = response.user.username

    links = Link.objects.all().filter(owner=user)

    if response.method == "POST":
        if "add_link" in response.POST:
            new_company = response.POST.get("company", "")
            new_product = response.POST.get("product_name", "")
            new_url = response.POST.get("url", "")
            new_threshold = response.POST.get("threshold", "")

            link_add = Link(url=new_url, store=new_company, threshold=new_threshold, active="True", title=new_product, owner=user)
            link_add.save()
            return redirect("dashboard:view")

    return render(response, "dashboard/view.html", {"username":username, "links":links})


def delete(response, linkid):

    if response.user.is_authenticated:
        user = response.user

    if response.method == "POST":
        if "delete_link" in response.POST:
            Link.objects.all().filter(owner=user).get(pk=linkid).delete()

    return redirect("dashboard:view")