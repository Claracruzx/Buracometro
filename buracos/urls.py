from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('cadastrar', cadastroView, name='cadastrarView'),
    path('cadastrar/selecionar-local', cadastroSelecionarLocalView, name='cadastroSelecionarLocalView'),
    path('cadastrar/selecionar-local/selecionando', passarLocalParaCadastroView, name='passarLocalParaCadastroView'),
    path('cadastrar/salvar', cadastroStore, name='cadastroStore'),
    path('popular', popularView, name='popularView'),
    path('explorar', explorarView, name='explorarView'),
    path('detalhe/<int:id>/', detalheBuracoView, name='detalheBuracoView'),
    path('excluir/<int:buraco_id>/', excluirBuracoView, name='excluirBuraco'),
    path('curtir/<int:buraco_id>/', curtirBuracoView, name='curtirBuraco'),
    path('reportar/<int:buraco_id>/', reportarBuracoView, name='reportarBuraco'),
    path('comentar/<int:buraco_id>/', comentarBuracoView, name='comentarBuraco'),
    path('comentario/<int:comentario_id>/curtir/', curtirComentarioView, name='curtirComentario'),
    path('comentario/<int:comentario_id>/excluir/', excluirComentarioView, name='excluirComentario'),
    ]
