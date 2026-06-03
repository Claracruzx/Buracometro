from django.db import models
from django.conf import settings


class Notificacao(models.Model):
    TIPO_CHOICES = [
        ("like", "Curtida"),
        ("like_comentario", "Curtida em comentario"),
        ("comentario", "Comentario"),
        ("resposta_comentario", "Resposta em comentario"),
        ("status", "Status"),
        ("remocao", "Remocao"),
    ]

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes_recebidas"
    )
    ator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes_enviadas",
        null=True,
        blank=True
    )
    buraco = models.ForeignKey(
        "buracos.Buraco",
        on_delete=models.SET_NULL,
        related_name="notificacoes",
        null=True,
        blank=True
    )
    comentario = models.ForeignKey(
        "buracos.Comentario",
        on_delete=models.CASCADE,
        related_name="notificacoes",
        null=True,
        blank=True
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensagem = models.CharField(max_length=255)
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["destinatario", "lida", "-created_at"], name="notif_dest_lida_created_idx"),
            models.Index(fields=["destinatario", "-created_at"], name="notif_dest_created_idx"),
        ]

    def __str__(self):
        return self.mensagem
