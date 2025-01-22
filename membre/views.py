from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SalonForm
from .models import *
from .forms import *

# Create your views here.


def pageInscription(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Compte créé avec succès pour' + user)
            return redirect('connection')

    context = {'form':form,}
    return render(request, 'inscription.html', context)

def pageConnection(request):

    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')

    context = {}
    return render(request, 'connection.html', context)


def membre(request):
    mesMembres = Membre.objects.all().values()
    template = loader.get_template('membres.html')
    context = {
        'mesMembres': mesMembres,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    mesMembres = Membre.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mesMembres': mesMembres,
    }
    return HttpResponse(template.render(context, request))

def Home(request):
    nombre_membres = Membre.count_members()
    return render(request, 'index.html', {'nombre_membres': nombre_membres})

def salons_disponible(request):
    salons = Salon.objects.all()
    return render(request, 'salon.html', {'salons': salons})


def create_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_disponible')  # Redirigez vers la page des salons
    else:
        form = SalonForm()

    context = {'form': form}
    return render(request, 'create_salon.html', context)
