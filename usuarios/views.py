from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import re

from .models import CustomUser
from buracos.models import Buraco, Like

PERFIL_LIMIT = 24


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
    total_buracos = Buraco.objects.filter(usuario=usuario).count()
    buracos = Buraco.objects.filter(usuario=usuario).select_related("usuario").prefetch_related(
        "likes",
        "comentarios__usuario",
        "comentarios__likes",
        "comentarios__respostas__usuario",
        "comentarios__respostas__likes",
    ).order_by('-created_at')[:PERFIL_LIMIT]

    buracos = list(buracos)
    buracos_curtidos = set()

    if buracos:
        buracos_curtidos = set(
            Like.objects
            .filter(usuario=request.user, buraco_id__in=[buraco.id for buraco in buracos])
            .values_list("buraco_id", flat=True)
        )

    for buraco in buracos:
        buraco.curtido = buraco.id in buracos_curtidos

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'buracos': buracos,
        'total_buracos': total_buracos,
    })


def perfilPublicoView(request, username):
    usuario_perfil = get_object_or_404(CustomUser, username=username)
    total_buracos = Buraco.objects.filter(usuario=usuario_perfil).count()
    buracos = Buraco.objects.filter(usuario=usuario_perfil).select_related("usuario").prefetch_related(
        "likes",
        "comentarios__usuario",
        "comentarios__likes",
        "comentarios__respostas__usuario",
        "comentarios__respostas__likes",
    ).order_by('-created_at')[:PERFIL_LIMIT]

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

    return render(request, 'usuarios/perfil_publico.html', {
        'usuario_perfil': usuario_perfil,
        'buracos': buracos,
        'total_buracos': total_buracos,
    })


@login_required
def editarPerfilView(request):
    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "perfil":
            nome = request.POST.get("nome", "").strip()
            username = request.POST.get("username", "").strip()
            foto = request.FILES.get("foto")
            remover_foto = request.POST.get("remover_foto")

            if not nome or not username:
                messages.error(request, "Nome e nome de usuario nao podem ficar vazios.")
                return redirect("editarPerfilView")

            if len(username) > 150 or not re.fullmatch(r"[\w.@+-]+", username):
                messages.error(request, "Use apenas letras, numeros, ponto, underline, + ou - no nome de usuario.")
                return redirect("editarPerfilView")

            username_em_uso = CustomUser.objects.filter(
                username__iexact=username
            ).exclude(id=request.user.id).exists()

            if username_em_uso:
                messages.error(request, "Esse nome de usuario ja esta em uso.")
                return redirect("editarPerfilView")

            request.user.name = nome
            request.user.username = username

            if remover_foto:
                request.user.foto.delete(save=False)
                request.user.foto = None

            if foto:
                request.user.foto = foto

            request.user.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("perfilView")

        if acao == "senha":
            senha_atual = request.POST.get("senha_atual", "")
            nova_senha = request.POST.get("nova_senha", "")
            confirmar_senha = request.POST.get("confirmar_senha", "")

            if not senha_atual or not nova_senha or not confirmar_senha:
                messages.error(request, "Preencha todos os campos para alterar a senha.")
                return redirect("editarPerfilView")

            if not request.user.check_password(senha_atual):
                messages.error(request, "A senha atual nao esta correta.")
                return redirect("editarPerfilView")

            if nova_senha != confirmar_senha:
                messages.error(request, "As novas senhas nao conferem.")
                return redirect("editarPerfilView")

            request.user.set_password(nova_senha)
            request.user.save(update_fields=["password"])
            update_session_auth_hash(request, request.user)
            messages.success(request, "Senha alterada com sucesso.")
            return redirect("editarPerfilView")

        if acao == "excluir":
            senha = request.POST.get("senha_exclusao", "")

            if not request.user.check_password(senha):
                messages.error(request, "Senha incorreta. A conta nao foi excluida.")
                return redirect("editarPerfilView")

            usuario = request.user
            logout(request)
            usuario.delete()
            messages.success(request, "Sua conta foi excluida com sucesso.")
            return redirect("login")

        messages.error(request, "Acao invalida.")
        return redirect("editarPerfilView")

    return render(request, "usuarios/editar_perfil.html")
