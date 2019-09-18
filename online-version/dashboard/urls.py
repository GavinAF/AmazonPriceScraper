from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [

path("", views.dashboard, name="dashboard"),
path("user/", views.profile, name="profile"),
path("view/", views.view_links, name="view"),
path("delete/", views.delete),
path("delete/<slug:linkid>", views.delete, name="delete"),
path("update/", views.link_update),
path("update/<slug:linkid>", views.link_update, name="update"),

]