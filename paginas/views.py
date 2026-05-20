from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "paginas/index.html"

class LoginView(TemplateView):
    template_name = "paginas/login.html"

class RegisterView(TemplateView):
    template_name = "paginas/register.html"