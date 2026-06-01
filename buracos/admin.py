from django.contrib import admin

from .models import Buraco, Comentario, Like, LikeComentario, Reporte


@admin.register(Buraco)
class BuracoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "status", "tamanho", "created_at")
    list_filter = ("status", "tamanho", "created_at")
    search_fields = ("titulo", "descricao", "endereco", "usuario__username")
    readonly_fields = ("created_at", "updated_at", "data_atual")


admin.site.register(Comentario)
admin.site.register(Like)
admin.site.register(LikeComentario)
admin.site.register(Reporte)
