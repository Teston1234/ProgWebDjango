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
from django.contrib.auth.models import User
# Create your views here.


def Home(request):
    return render(request, 'salon.html')

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
        return render(request, 'register.html', context)

def pageConnection(request):
    if request.user.is_authenticated:
        return redirect('salon_disponible')
    else:
        if request.method == 'POST':
            username =request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request=request, username=username, password=password)


            if user is not None:
                login(request, user)
                return redirect('salon_disponible')
            else:
                messages.info(request, 'Nom d\'utilisateur ou mot de passe incorrect')

        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('connection')


@login_required(login_url='connection')
def membre(request):
    mesMembres = User.objects.all()
    context = {
        'mesMembres': mesMembres,
    }
    return render (request, 'membres.html', context)

   

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


@login_required(login_url='connection')
def edit_salon(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    
    # Vérifie que l'utilisateur est bien le créateur du salon
    if salon.created_by != request.user:
        raise PermissionDenied("Vous n'êtes pas autorisé à modifier ce salon.")

    if request.method == 'POST':
        form = EditSalonForm(request.POST, instance=salon)
        if form.is_valid():
            # Enregistrer le salon sans les utilisateurs
            salon = form.save(commit=False)

            # Gestion des utilisateurs
            user_input = form.cleaned_data['users']
            usernames = [name.strip() for name in user_input.split(',') if name.strip()]
            users = User.objects.filter(username__in=usernames)

            if len(users) != len(usernames):
                # Trouve les utilisateurs invalides pour donner un message d'erreur précis
                invalid_usernames = set(usernames) - set(users.values_list('username', flat=True))
                messages.error(
                    request,
                    f"Les noms d'utilisateur suivants sont invalides : {', '.join(invalid_usernames)}"
                )
                return render(request, 'edit_salon.html', {'form': form, 'salon': salon})

            # Associer les utilisateurs au salon
            salon.save()  # Sauvegarde le salon pour obtenir l'ID
            salon.users.set(users)  # Remplace les utilisateurs existants

            messages.success(request, "Le salon a été modifié avec succès.")
            return redirect('view_salon', salon_id=salon.id)
    else:
        # Pré-remplir le champ "users" avec les noms des utilisateurs existants
        initial_users = ', '.join(salon.users.values_list('username', flat=True))
        form = EditSalonForm(instance=salon, initial={'users': initial_users})

    context = {'form': form, 'salon': salon}
    return render(request, 'edit_salon.html', context)