from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q

from buracos.models import Buraco, Like
from usuarios.models import CustomUser


def inicioView(request):
    buracos = Buraco.objects.all().order_by('-created_at')

    for buraco in buracos:
        buraco.curtido = Like.objects.filter(
            usuario=request.user,
            buraco=buraco
        ).exists()

    variaveis = {
        'buracos': buracos,
    }

    return render(request, 'principal/inicio.html', variaveis)





class VerNoMapaView(TemplateView):
    template_name = "principal/ver-no-mapa.html"


def deslogar(request):
    logout(request)
    return redirect(reverse('login'))


def pesquisaView(request):
    termo = request.GET.get('q', '')

    usuarios = CustomUser.objects.filter(
        Q(username__icontains=termo) |
        Q(name__icontains=termo)
    ) if termo else []

    buracos = Buraco.objects.filter(
        Q(endereco__icontains=termo) |
        Q(local__icontains=termo) |
        Q(titulo__icontains=termo)
    ) if termo else []

    return render(request, 'principal/pesquisa.html', {
        'termo': termo,
        'usuarios': usuarios,
        'buracos': buracos,
    })