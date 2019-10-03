from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [

path("", views.dashboard, name="dashboard"),
path("user/", views.profile, name="profile"),
path("view/", views.view_links, name="view"),
path("delete/", views.delete),
path("delete/<slug:linkid>", views.delete, name="delete"),
path("update/", views.update, name="update"),
path("modal/<slug:linkid>", views.modal, name="modal"),
path("update_table/", views.update_table, name="update_table"),
path("create/", views.create, name="create")

]