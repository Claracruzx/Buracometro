from django.db import models
# AJUSTE: Adicionada a importação do UserManager
from django.contrib.auth.models import AbstractUser, UserManager 

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='perfis/', null=True, blank=True)
    postagens_removidas_por_reporte = models.PositiveIntegerField(default=0)

    # AJUSTE: Linha obrigatória para que o create_user criptografe a senha
    objects = UserManager() 

    def __str__(self):
        return self.username

    @property
    def verificado(self):
        if self.is_staff or self.is_superuser or self.postagens_removidas_por_reporte > 0:
            return False

        from buracos.models import Buraco

        buracos = Buraco.objects.filter(usuario=self)
        return (
            buracos.count() >= 5
            and buracos.filter(status=Buraco.STATUS_ARRUMADO).exists()
        )
