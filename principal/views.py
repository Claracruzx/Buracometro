from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from buracos.models import Buraco


def inicioView(request):
    buracos = Buraco.objects.all().order_by('-created_at')

    variaveis = {
        'buracos': buracos,
    }

    return render(request, 'principal/inicio.html', variaveis)

#class RankingView(TemplateView):
  #  template_name = "principal/ranking.html"

def rankingView(request):
    buracos = Buraco.objects.order_by('-tamanho')
    variaveis = {
        'buracos':buracos,
    }
    return render(request, 'principal/ranking.html', variaveis)

class VerNoMapaView(TemplateView):
    template_name = "principal/ver-no-mapa.html"

# def deslogar(request):
def deslogar(request):
    logout(request) 
    return redirect(reverse('inicio'))