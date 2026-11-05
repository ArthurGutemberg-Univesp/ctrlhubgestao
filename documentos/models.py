from django.db import models
from core.models import Cliente, CustomUser

class Documento(models.Model):
    CATEGORIA_CHOICES = [
        ('FISCAL', 'Documento Fiscal'),
        ('CONTRATO', 'Contrato'),
        ('FOLHA', 'Folha de Pagamento'),
        ('OUTROS', 'Outros'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='OUTROS')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='documentos')
    arquivo_atual = models.FileField(upload_to='documentos/%Y/%m/')
    versao_atual = models.PositiveIntegerField(default=1)
    responsavel = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_modificacao']

    def __str__(self):
        return f"{self.titulo} v{self.versao_atual} - {self.cliente.razao_social}"

class VersaoDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='versoes')
    arquivo = models.FileField(upload_to='versoes/%Y/%m/')
    numero_versao = models.PositiveIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    comentario = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-numero_versao']
        unique_together = ['documento', 'numero_versao']

    def __str__(self):
        return f"Versão {self.numero_versao} de {self.documento.titulo}"