from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="Home"),
    path("membre/", views.membre, name="membre"),
    path("membre/details/<int:id>", views.details, name="details"),

    path("membre/connection", views.pageConnection, name="connection"),
    path("membre/inscription", views.pageInscription, name="inscription"),
    path("membre/logout", views.logoutUser, name="logout"),

    path("membre/salon", views.salons_disponible, name="salon_disponible"),
    path('membre/salon/create', views.create_salon, name='create_salon'),
]