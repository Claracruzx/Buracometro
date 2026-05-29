from django.db import models
from django.conf import settings

class Buraco(models.Model):
    titulo = models.CharField(max_length=255) 
    descricao = models.TextField()  
    local = models.CharField(max_length=255)  
    endereco = models.CharField(max_length=255)
    url_imagem = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='buracos/', null=True, blank=True)
    tamanho = models.SmallIntegerField(default=1)
    data_atual = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação (preenchido automaticamente)
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora de última atualização (atualizado automaticamente)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo

    @property
    def tamanho_nome(self):
        tamanhos = {
            1: "Pequeno",
            2: "Médio",
            3: "Grande",
            4: "Gigante",
        }

        return tamanhos.get(self.tamanho, "Pequeno")

class Like(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    buraco = models.ForeignKey(
        Buraco,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'buraco')


class Comentario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    buraco = models.ForeignKey(
        Buraco,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    texto = models.TextField()
    resposta_de = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="respostas",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class LikeComentario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comentario = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'comentario')


class Reporte(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    buraco = models.ForeignKey(
        Buraco,
        on_delete=models.CASCADE,
        related_name="reportes"
    )
    motivo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'buraco')
