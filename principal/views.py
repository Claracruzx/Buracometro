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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pontos = []
        zonas = {}

        for buraco in Buraco.objects.exclude(local__isnull=True).exclude(local=""):
            coordenadas = [parte.strip() for parte in buraco.local.split(",")]

            if len(coordenadas) < 2:
                continue

            try:
                latitude = float(coordenadas[0])
                longitude = float(coordenadas[1])
            except ValueError:
                continue

            zona = self.extrair_zona(buraco.endereco)

            pontos.append({
                "id": buraco.id,
                "titulo": buraco.titulo,
                "descricao": buraco.descricao,
                "endereco": buraco.endereco,
                "latitude": latitude,
                "longitude": longitude,
                "zona": zona,
                "likes": buraco.likes.count(),
                "comentarios": buraco.comentarios.count(),
                "url": reverse("detalheBuracoView", args=[buraco.id]),
            })

            if zona not in zonas:
                zonas[zona] = {
                    "nome": zona,
                    "quantidade": 0,
                    "soma_latitude": 0,
                    "soma_longitude": 0,
                }

            zonas[zona]["quantidade"] += 1
            zonas[zona]["soma_latitude"] += latitude
            zonas[zona]["soma_longitude"] += longitude

        context["pontos_mapa"] = pontos
        context["zonas_mapa"] = [
            {
                "nome": zona["nome"],
                "quantidade": zona["quantidade"],
                "latitude": zona["soma_latitude"] / zona["quantidade"],
                "longitude": zona["soma_longitude"] / zona["quantidade"],
            }
            for zona in sorted(zonas.values(), key=lambda item: item["quantidade"], reverse=True)
        ]

        return context

    @staticmethod
    def extrair_zona(endereco):
        partes = [
            parte.split(" - ")[0].strip()
            for parte in endereco.split(",")
            if parte.strip()
        ]

        ignorar = {"brasil", "maranhão", "são luís", "região nordeste"}

        for parte in reversed(partes):
            if parte.lower() not in ignorar:
                return parte

        return "Local não identificado"


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
