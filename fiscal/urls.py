from django.urls import path
from . import views

urlpatterns = [
    path('obrigacoes/', views.lista_obrigacoes, name='lista_obrigacoes'),
    path('calendario/', views.pagina_calendario, name='pagina_calendario'),
    path('api/eventos/', views.calendario_fiscal, name='api_eventos_calendario'),
]