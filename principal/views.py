from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

from buracos.models import Buraco, Like
from .models import Notificacao
from usuarios.models import CustomUser

FEED_LIMIT = 30
MAPA_LIMIT = 120
PESQUISA_LIMIT = 30
NOTIFICACOES_LIMIT = 60


STATUS_FILTROS = [
    ("", "Todos"),
    (Buraco.STATUS_NAO_ARRUMADO, "Ainda não arrumados"),
    (Buraco.STATUS_EM_OBRA, "Em obra"),
    (Buraco.STATUS_ARRUMADO, "Já arrumados"),
]


def filtrar_buracos_por_status(queryset, status):
    status_validos = {valor for valor, _ in Buraco.STATUS_CHOICES}

    if status in status_validos:
        return queryset.filter(status=status)

    return queryset


def inicioView(request):
    status_atual = request.GET.get("status", "")
    buracos = filtrar_buracos_por_status(
        Buraco.objects
        .select_related("usuario")
        .prefetch_related(
            "likes",
            "comentarios__usuario",
            "comentarios__likes",
            "comentarios__respostas__usuario",
            "comentarios__respostas__likes",
        ),
        status_atual
    ).order_by('-created_at')[:FEED_LIMIT]

    buracos = list(buracos)
    buracos_curtidos = set()

    if request.user.is_authenticated and buracos:
        buracos_curtidos = set(
            Like.objects
            .filter(usuario=request.user, buraco_id__in=[buraco.id for buraco in buracos])
            .values_list("buraco_id", flat=True)
        )

    for buraco in buracos:
        buraco.curtido = buraco.id in buracos_curtidos

    variaveis = {
        'buracos': buracos,
        'status_atual': status_atual,
        'status_filtros': STATUS_FILTROS,
    }

    return render(request, 'principal/inicio.html', variaveis)





class VerNoMapaView(TemplateView):
    template_name = "principal/ver-no-mapa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pontos = []
        zonas = {}
        status_atual = self.request.GET.get("status", "")
        buracos = filtrar_buracos_por_status(
            Buraco.objects
            .exclude(local__isnull=True)
            .exclude(local="")
            .annotate(
                total_likes=Count("likes", distinct=True),
                total_comentarios=Count("comentarios", distinct=True),
            ),
            status_atual
        ).order_by("-created_at")[:MAPA_LIMIT]

        for buraco in buracos:
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
                "status": buraco.status_nome,
                "status_classe": buraco.status_classe,
                "likes": buraco.total_likes,
                "comentarios": buraco.total_comentarios,
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
        context["status_atual"] = status_atual
        context["status_filtros"] = STATUS_FILTROS
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
    status_atual = request.GET.get("status", "")

    usuarios = CustomUser.objects.filter(
        Q(username__icontains=termo) |
        Q(name__icontains=termo)
    )[:PESQUISA_LIMIT] if termo else []

    buracos = filtrar_buracos_por_status(Buraco.objects.filter(
        Q(endereco__icontains=termo) |
        Q(local__icontains=termo) |
        Q(titulo__icontains=termo) |
        Q(descricao__icontains=termo)
    ), status_atual).select_related("usuario").prefetch_related("likes", "comentarios").order_by("-created_at")[:PESQUISA_LIMIT] if termo else []

    return render(request, 'principal/pesquisa.html', {
        'termo': termo,
        'usuarios': usuarios,
        'buracos': buracos,
        'status_atual': status_atual,
        'status_filtros': STATUS_FILTROS,
    })


@login_required
def notificacoesView(request):
    notificacoes = list(
        Notificacao.objects
        .filter(destinatario=request.user)
        .select_related("ator", "buraco", "comentario")
        .order_by("-created_at")[:NOTIFICACOES_LIMIT]
    )

    Notificacao.objects.filter(destinatario=request.user, lida=False).update(lida=True)

    return render(request, "principal/notificacoes.html", {
        "notificacoes": notificacoes,
    })
