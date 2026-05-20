from django.urls import path
from .views import LoginView, RegisterView, registerStore, loginAction, logoutAction, perfilView, perfilPublicoView

urlpatterns = [
    # path('', IndexView.as_view(), name='inicio'),
    path('login', LoginView.as_view(), name='login'),
    path('login/logar', loginAction, name='loginAction'),
    path('cadastro', RegisterView.as_view(), name='register'),
    path('cadastro/cadastrar', registerStore, name='registerStore'),
    path('logout/', logoutAction, name='logout'),
    path('perfil/', perfilView, name='perfilView'),
    path('perfil/<str:username>/', perfilPublicoView, name='perfilPublicoView'),
]