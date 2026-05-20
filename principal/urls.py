from django.contrib import admin
from django.urls import path, include
from .views import InicioView, rankingView, VerNoMapaView, deslogar

urlpatterns = [
    path('', InicioView.as_view(), name='inicioView'),
    path('/inicio', InicioView.as_view(), name='inicioView'),
    path('/ranking', rankingView, name='rankingView'),
    path('/ver-no-mapa', VerNoMapaView.as_view(), name='verNoMapaView'),
    path('/logout', deslogar, name='deslogar'),
]