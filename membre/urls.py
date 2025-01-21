from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="Home"),
    path("membre/", views.membre, name="membre"),
    path("membre/details/<int:id>", views.details, name="details"),
]