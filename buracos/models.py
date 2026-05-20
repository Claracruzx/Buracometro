from django.db import models
from django.conf import settings

class Buraco(models.Model):
    titulo = models.CharField(max_length=255) 
    descricao = models.TextField()  
    local = models.CharField(max_length=255)  
    endereco = models.CharField(max_length=255)
    url_imagem = models.URLField()
    tamanho = models.SmallIntegerField(default=1)
    data_atual = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação (preenchido automaticamente)
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora de última atualização (atualizado automaticamente)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo