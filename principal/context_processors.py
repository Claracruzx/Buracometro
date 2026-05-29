from .models import Notificacao


def notificacoes_nao_lidas(request):
    if not request.user.is_authenticated:
        return {"notificacoes_nao_lidas": 0}

    return {
        "notificacoes_nao_lidas": Notificacao.objects.filter(
            destinatario=request.user,
            lida=False
        ).count()
    }
