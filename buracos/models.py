from django.db import models
from django.conf import settings

class Buraco(models.Model):
    STATUS_NAO_ARRUMADO = "nao_arrumado"
    STATUS_EM_OBRA = "em_obra"
    STATUS_ARRUMADO = "arrumado"

    STATUS_CHOICES = [
        (STATUS_NAO_ARRUMADO, "Ainda nao foi arrumado"),
        (STATUS_EM_OBRA, "Em obra"),
        (STATUS_ARRUMADO, "Ja arrumado"),
    ]

    titulo = models.CharField(max_length=255) 
    descricao = models.TextField()  
    local = models.CharField(max_length=255)  
    endereco = models.CharField(max_length=255)
    url_imagem = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='buracos/', null=True, blank=True)
    tamanho = models.SmallIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NAO_ARRUMADO
    )
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

    @property
    def status_nome(self):
        return dict(self.STATUS_CHOICES).get(self.status, "Ainda nao foi arrumado")

    @property
    def status_classe(self):
        return self.status.replace("_", "-")

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"], name="buraco_created_idx"),
            models.Index(fields=["status", "-created_at"], name="buraco_status_created_idx"),
            models.Index(fields=["usuario", "-created_at"], name="buraco_usuario_created_idx"),
        ]

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

    class Meta:
        indexes = [
            models.Index(fields=["buraco", "resposta_de", "created_at"], name="coment_buraco_resp_idx"),
        ]


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
