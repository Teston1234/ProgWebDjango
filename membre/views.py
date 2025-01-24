from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import SalonForm
from .models import *
from .forms import *

# Create your views here.


def pageInscription(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
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
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        if request.method == 'POST':
            username =request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request=request, username=username, password=password)


            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.info(request, 'Nom d\'utilisateur ou mot de passe incorrect')

        context = {}
        return render(request, 'connection.html', context)

def logoutUser(request):
    logout(request)
    return redirect('connection')


@login_required(login_url='connection')
def membre(request):
    mesMembres = Membre.objects.all().values()
    template = loader.get_template('membres.html')
    context = {
        'mesMembres': mesMembres,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='connection')
def details(request, id):
    mesMembres = Membre.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mesMembres': mesMembres,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='connection')
def Home(request):
    nombre_membres = Membre.count_members()
    return render(request, 'index.html', {'nombre_membres': nombre_membres})

@login_required(login_url='connection')
def salons_disponible(request):
    salons = Salon.objects.all()
    return render(request, 'salon.html', {'salons': salons})


@login_required(login_url='connection')
def create_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.created_by = request.user  # L'utilisateur connecté devient le créateur
            salon.save()
            return redirect('view_salon', salon_id=salon.id)  # Redirige vers le salon créé
    else:
        form = SalonForm()

    context = {'form': form}
    return render(request, 'create_salon.html', context)



@login_required(login_url='connection')
def view_salon(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(salon=salon, user=request.user, contenu=contenu)

    return render(request, 'view_salon.html', {'salon': salon})

@login_required(login_url='connection')
def delete_salon(request, salon_id):
        salon = Salon.objects.get(id=salon_id)
        if salon.created_by == request.user:  # Vérifie que l'utilisateur est le créateur
            salon.delete()
        else:
            messages.error(request, "Vous n'êtes pas autorisé à supprimer ce salon.")
        return redirect('salon_disponible')

@login_required(login_url='connection')

@login_required(login_url='connection')
def ajouter_membre(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    if salon.created_by != request.user:
        raise PermissionDenied("Vous n'êtes pas autorisé à ajouter des membres à ce salon.")

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_to_add = User.objects.get(username=username)
            if user_to_add not in salon.users.all():
                salon.users.add(user_to_add)
                messages.success(request, f"L'utilisateur {user_to_add.username} a été ajouté au salon.")
            else:
                messages.info(request, "Cet utilisateur est déjà membre du salon.")
        except User.DoesNotExist:
            messages.error(request, "L'utilisateur avec ce nom d'utilisateur n'existe pas.")
        
    return redirect('view_salon', salon_id=salon_id)


