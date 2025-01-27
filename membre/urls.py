from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.salons_disponible, name="Home"),
    path("membre/", views.membre, name="membre"),
    path("membre/details/<int:id>", views.details, name="details"),
    path('membre/connection/', views.pageConnection, name='pageConnection'),
    path("membre/connection", views.pageConnection, name="connection"),
    path("membre/inscription", views.pageInscription, name="inscription"),
    path("membre/logout", views.logoutUser, name="logout"),
    
    path('membre/salon/<int:salon_id>/', views.view_salon, name='view_salon'),
    path("membre/salon", views.salons_disponible, name="salon_disponible"),
    path('membre/salon/create', views.create_salon, name='create_salon'),
    path('membre/salon/delete/<int:salon_id>/', views.delete_salon, name='delete_salon'),
    path('membre/salon/ajouter_membre/<int:salon_id>/', views.ajouter_membre, name='ajouter_membre'),
    path('membre/salon/<int:salon_id>/edit/', views.edit_salon, name='edit_salon'),
]