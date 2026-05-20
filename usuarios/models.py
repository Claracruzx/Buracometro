from django.db import models
# AJUSTE: Adicionada a importação do UserManager
from django.contrib.auth.models import AbstractUser, UserManager 

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    # AJUSTE: Linha obrigatória para que o create_user criptografe a senha
    objects = UserManager() 

    def __str__(self):
        return self.username
