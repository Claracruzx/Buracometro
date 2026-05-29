from django.urls import path
from .views import inicioView, VerNoMapaView, deslogar, pesquisaView, notificacoesView

urlpatterns = [
    path('', inicioView, name='inicioView'),
    path('inicio', inicioView, name='inicioView'),
    path('ver-no-mapa', VerNoMapaView.as_view(), name='verNoMapaView'),
    path('logout', deslogar, name='deslogar'),
    path('pesquisa/', pesquisaView, name='pesquisaView'),
    path('notificacoes/', notificacoesView, name='notificacoesView'),
]
