from django.shortcuts import render, redirect, get_object_or_404
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

def link_update(response, linkid):

    if response.method == "POST":
        if "update_link" in response.POST:
            id_link = response.POST.get("linkid", "")
            new_company = response.POST.get("company", "")
            new_product = response.POST.get("product_name", "")
            new_url = response.POST.get("url", "")
            new_threshold = response.POST.get("threshold", "")

            link_modify = Link.objects.all().filter(owner=user).get(pk=id_link)

            if link_modify.store != new_company:
                link_modify.store = new_company

            if link_modify.title != new_product:
                link_modify.title = new_product

            if link_modify.url != new_url:
                link_modify.url = new_url

            if link_modify.threshold != new_threshold:
                link_modify.threshold = new_threshold

            link_modify.save()

    if response.user.is_authenticated:
        user = response.user
    
    instance = get_object_or_404(Link.objects.all().filter(owner=user), pk=linkid)
    context={
        'instance':instance
    }
    
    return render(response, "dashboard/modal.html", context)