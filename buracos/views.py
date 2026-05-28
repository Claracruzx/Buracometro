from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Buraco, Like, Comentario, Reporte
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone


def cadastroView(request):
    titulo = request.GET.get('titulo', '')
    descricao = request.GET.get('descricao', '')
    tamanho = request.GET.get('tamanho', '1')
    coordenadas = request.GET.get('coordenadas', '') 
    endereco = request.GET.get('endereco', '')

    variaveis = {
        'titulo': titulo,
        'descricao': descricao,
        'tamanho': tamanho,
        'coordenadas': coordenadas,
        'endereco': endereco,
    }

    return render(request, 'buracos/cadastro.html', variaveis)


def cadastroSelecionarLocalView(request):
    titulo = ''
    descricao = ''
    tamanho = '1'

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        tamanho = request.POST.get("tamanho")

    variaveis = {
        'titulo': titulo,
        'descricao': descricao,
        'tamanho': tamanho,
    }

    return render(request, "buracos/cadastro-selecionar-local.html", variaveis)


def explorarView(request):
    buracos = Buraco.objects.all()
    variaveis = {
        'rows': buracos,
    }
    return render(request, 'buracos/explorar.html', variaveis)

def passarLocalParaCadastroView(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        tamanho = request.POST.get("tamanho")
        coordenadas = request.POST.get("coordenadas")
        endereco = request.POST.get("endereco")

        parametros = {
            'titulo': titulo,
            'descricao': descricao,
            'tamanho': tamanho,
            'coordenadas': coordenadas,
            'endereco': endereco,
        }

        url = reverse('cadastrarView') + '?' + urlencode(parametros)  # Adiciona os parâmetros à URL

    return redirect(url)

@login_required
def cadastroStore(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        coordenadas = request.POST.get("coordenadas")
        endereco = request.POST.get("endereco")
        tamanho = request.POST.get("tamanho")
        imagem = request.FILES.get("imagem")

        if not imagem:
            messages.error(request, "A imagem do buraco é obrigatória.")
            return redirect("cadastrarView")

        if not coordenadas or not endereco:
            messages.error(request, "Selecione a localização do buraco no mapa.")
            return redirect("cadastrarView")

        try:
            Buraco.objects.create(
                titulo=titulo,
                descricao=descricao,
                local=coordenadas,
                endereco=endereco,
                tamanho=tamanho,
                imagem=imagem,
                usuario=request.user,
            )

            msg = "Buraco cadastrado com sucesso!"
            messages.success(request, msg)

        except IntegrityError as e:
            msg = f"Erro ao criar buraco: {e}"
            messages.error(request, msg)

    return redirect('cadastrarView')


def detalheBuracoView(request, id):
    buraco = Buraco.objects.get(id=id)

    return render(request, 'buracos/detalhe-buraco.html', {
        'buraco': buraco
    }) 

@login_required
def curtirBuracoView(request, buraco_id):
    buraco = get_object_or_404(Buraco, id=buraco_id)

    like, created = Like.objects.get_or_create(
        usuario=request.user,
        buraco=buraco
    )

    curtido = True

    if not created:
        like.delete()
        curtido = False

    return JsonResponse({
        'likes': buraco.likes.count(),
        'curtido': curtido
    })
    
@login_required
def reportarBuracoView(request, buraco_id):

    buraco = get_object_or_404(Buraco, id=buraco_id)

    reporte, created = Reporte.objects.get_or_create(
        usuario=request.user,
        buraco=buraco
    )

    if buraco.reportes.count() >= 5:
        buraco.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def comentarBuracoView(request, buraco_id):

    if request.method == "POST":

        buraco = get_object_or_404(Buraco, id=buraco_id)

        texto = request.POST.get("comentario", "").strip()

        if texto:

            comentario = Comentario.objects.create(
                usuario=request.user,
                buraco=buraco,
                texto=texto
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                foto_url = request.user.foto.url if getattr(request.user, "foto", None) else ""

                return JsonResponse({
                    "id": comentario.id,
                    "texto": comentario.texto,
                    "username": request.user.username,
                    "foto_url": foto_url,
                    "inicial": request.user.username[:1].upper(),
                    "data": timezone.localtime(comentario.created_at).strftime("%d/%m/%Y %H:%M"),
                    "total_comentarios": buraco.comentarios.count(),
                })

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"erro": "Comentário vazio."}, status=400)

    return redirect(request.META.get('HTTP_REFERER'))
