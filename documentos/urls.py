from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_documentos, name='lista_documentos'),
    path('upload/', views.upload_documento, name='upload_documento'),
    path('<int:pk>/', views.detalhe_documento, name='detalhe_documento'),
    path('<int:pk>/nova-versao/', views.nova_versao, name='nova_versao'),
    path('relatorio/', views.relatorio_documentos, name='relatorio_documentos'),
]