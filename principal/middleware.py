from django.urls import reverse
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        urls_liberadas = [
            '/', 
            reverse('login'), 
            reverse('register'), 
        ]

        # AJUSTE: Corrigido '/cadastrar' para '/cadastro' e adicionado tratamento para arquivos estáticos
        if not request.user.is_authenticated \
            and request.path not in urls_liberadas \
            and not request.path.startswith((
                '/admin',
                '/login',
                '/cadastro',   # Libera a rota de processamento do cadastro (/cadastro/cadastrar)
                '/static/',    # Libera os arquivos CSS/JS na tela de login
                '/media/'      # Libera imagens de mídia se houver
            )):
            return redirect(reverse('login'))
        
        response = self.get_response(request)
        return response
