from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from buracos.models import Buraco, Like


class LoginView(TemplateView):
    template_name = "usuarios/login.html"


class RegisterView(TemplateView):
    template_name = "usuarios/register.html"


def registerStore(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        usuario = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")
        dataNascimento = request.POST.get("data-nascimento") or None
        dados_formulario = {
            "nome": nome,
            "usuario_digitado": usuario,
        }

        if not nome or not usuario or not senha or not confirmar_senha:
            messages.error(request, "Preencha todos os campos antes de criar sua conta.")
            return render(request, "usuarios/register.html", dados_formulario)

        if senha != confirmar_senha:
            messages.error(request, "As senhas nao conferem.")
            return render(request, "usuarios/register.html", dados_formulario)

        try:
            if CustomUser.objects.filter(username=usuario).exists():
                messages.error(request, "Esse nome de usuario ja esta em uso.")
                return render(request, "usuarios/register.html", dados_formulario)

            user = CustomUser(
                username=usuario,
                name=nome,
                date_of_birth=dataNascimento
            )
            user.set_password(senha)
            user.save()

            messages.success(request, "Usuario criado com sucesso! Faca login.")
            return redirect("login")

        except Exception as e:
            print("ERRO AO CADASTRAR:", e)
            messages.error(request, f"Erro ao criar usuario: {e}")
            return render(request, "usuarios/register.html", dados_formulario)

    return redirect("register")


def loginAction(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario", "").strip()
        senha = request.POST.get("senha", "")

        if not usuario or not senha:
            messages.error(request, "Preencha usuario e senha para entrar.")
            return render(request, "usuarios/login.html", {
                "usuario_digitado": usuario,
            })

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect("inicioView")

        messages.error(request, "Usuario e/ou senha invalidos.")
        return render(request, "usuarios/login.html", {
            "usuario_digitado": usuario,
        })

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
