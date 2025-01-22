from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *

# Create your views here.


def pageInscription(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/connection.html')

    context = {'form':form,}
    return render(request, 'inscription.html', context)

def pageConnection(request):
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