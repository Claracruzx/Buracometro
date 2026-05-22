from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import os
import shutil
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from datetime import datetime
from .models import Buraco
from django.contrib.auth.decorators import login_required

# class CadastroView(TemplateView):
#     template_name = "buracos/cadastro.html"


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

# class CadastroSelecionarLocalView(TemplateView):
#     template_name = "buracos/cadastro-selecionar-local.html"

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

# class VerBuracosView(TemplateView):
#     template_name = "buracos/ver-buracos.html"

def verBuracosView(request):
    buracos = Buraco.objects.all()
    variaveis = {
        'rows': buracos,
    }
    return render(request, 'buracos/ver-buracos.html', variaveis)

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
        imagem = request.FILES["imagem"]

        caminho_pasta = os.path.join(settings.BASE_DIR, 'paginas/static/paginas/image-users')  # Pasta de destino
        nome_arquivo = imagem.name

        os.makedirs(caminho_pasta, exist_ok=True)

        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

        if os.path.exists(caminho_arquivo):
            base_nome, extensao = os.path.splitext(nome_arquivo)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            nome_arquivo = f"{base_nome}_{timestamp}{extensao}"
            caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

        try:
            buraco = Buraco.objects.create (
                titulo = titulo,
                descricao = descricao,
                local = coordenadas,
                endereco = endereco,
                tamanho = tamanho,
                url_imagem = nome_arquivo,
                usuario=request.user,
            )

            buraco.save()

            with open(caminho_arquivo, 'wb+') as destino:
                shutil.copyfileobj(imagem.file, destino)

            msg = "Buraco cadastrado com sucesso! " \
                f"Veja mais em <a href='{reverse('verBuracosView')}'>seus buracos</a>"
            messages.success(request, msg)
        except IntegrityError as e:
            msg = f"Erro ao criar buraco: {e}"
            messages.error(request, msg)

        # print(titulo)
        # print(descricao)
        # print(endereco)
        # print(coordenadas)
        # print(tamanho)
        # print(imagem)
        # print(nome_arquivo)

    return redirect('cadastrarView')   

def detalheBuracoView(request, id):
    buraco = Buraco.objects.get(id=id)

    return render(request, 'buracos/detalhe-buraco.html', {
        'buraco': buraco
    }) 