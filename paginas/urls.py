from django.urls import path
from .views import IndexView
# from .views import IndexView, LoginView, RegisterView

urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    # path('login', LoginView.as_view(), name='login'),
    # path('cadastro', RegisterView.as_view(), name='register'),
]