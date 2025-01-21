from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Membre
from django.shortcuts import render

# Create your views here.

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

def testing(request):
    mesmembres = Membre.objects.all().values()
    template = loader.get_template('template.html')
    context = {
        'mesmembres': mesmembres,
    }
    return HttpResponse(template.render(context, request))