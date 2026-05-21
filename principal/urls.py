from django.urls import path
from .views import inicioView, rankingView, VerNoMapaView, deslogar, pesquisaView

urlpatterns = [
    path('', inicioView, name='inicioView'),
    path('inicio', inicioView, name='inicioView'),
    path('ranking', rankingView, name='rankingView'),
    path('ver-no-mapa', VerNoMapaView.as_view(), name='verNoMapaView'),
    path('logout', deslogar, name='deslogar'),
    path('pesquisa/', pesquisaView, name='pesquisaView'),
]