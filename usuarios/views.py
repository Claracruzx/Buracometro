from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
# AJUSTE: Incluída a importação do logout
from django.contrib.auth import authenticate, login, logout             
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from buracos.models import Buraco, Like

class LoginView(TemplateView):
    template_name = "usuarios/login.html"

class RegisterView(TemplateView):
    template_name = "usuarios/register.html"

def registerStore(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        dataNascimento = request.POST.get("data-nascimento")

        if not dataNascimento:
            dataNascimento = None 

        try:
            if CustomUser.objects.filter(username=usuario).exists():
                messages.error(request, "Esse nome de usuário já está em uso.")
                return redirect("register")

            # CORREÇÃO DEFINITIVA: Criamos o objeto sem salvar ainda
            user = CustomUser(
                username=usuario,
                name=nome,
                date_of_birth=dataNascimento
            )
            
            # Forçamos o Django a criptografar a senha manualmente
            user.set_password(senha)
            
            # Salvamos o usuário com a senha já criptografada
            user.save()

            messages.success(request, "Usuário criado com sucesso! Faça login.")
            return redirect("login")

        except Exception as e:
            print("ERRO AO CADASTRAR:", e)
            messages.error(request, f"Erro ao criar usuário: {e}")
            return redirect("register")

    return redirect("register")


def loginAction(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")

        print("--- TESTE DE LOGIN ---")
        print("USUARIO RECEBIDO DO HTML:", repr(usuario))
        print("SENHA RECEBIDA DO HTML:", repr(senha))


        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            # Garanta que a rota "inicioView" existe no seu urls.py
            return redirect("inicioView") 
        else:
            messages.error(request, "Usuário e/ou senha inválido(s).")

    return redirect("login")

def logoutAction(request):
    logout(request)
    return redirect("login")


@login_required
def perfilView(request):
    usuario = request.user

    buracos = Buraco.objects.filter(usuario=usuario).order_by('-created_at')

    for buraco in buracos:
        buraco.curtido = Like.objects.filter(
            usuario=request.user,
            buraco=buraco
        ).exists()

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'buracos': buracos,
    })

    return render(request, 'usuarios/perfil.html', variaveis)

from django.shortcuts import get_object_or_404

def perfilPublicoView(request, username):
    usuario_perfil = get_object_or_404(CustomUser, username=username)

    buracos = Buraco.objects.filter(usuario=usuario_perfil).order_by('-created_at')

    for buraco in buracos:
        buraco.curtido = request.user.is_authenticated and Like.objects.filter(
            usuario=request.user,
            buraco=buraco
        ).exists()

    return render(request, 'usuarios/perfil_publico.html', {
        'usuario_perfil': usuario_perfil,
        'buracos': buracos,
    })

@login_required
def editarPerfilView(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        foto = request.FILES.get("foto")
        remover_foto = request.POST.get("remover_foto")

        request.user.name = nome

        if remover_foto:
            request.user.foto.delete()
            request.user.foto = None

        if foto:
            request.user.foto = foto

        request.user.save()

        return redirect("perfilView")

    return render(request, "usuarios/editar_perfil.html")
