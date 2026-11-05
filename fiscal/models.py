from django.db import models
from core.models import Cliente, CustomUser

class ObrigacaoFiscal(models.Model):
    PERIODICIDADE_CHOICES = [
        ('MENSAL', 'Mensal'),
        ('TRIMESTRAL', 'Trimestral'),
        ('ANUAL', 'Anual'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='obrigacoes')
    tipo = models.CharField(max_length=100, help_text='Ex: DAS, DIRF, EFD-ICMS')
    periodicidade = models.CharField(max_length=20, choices=PERIODICIDADE_CHOICES)
    data_vencimento_base = models.DateField(help_text='Dia base do vencimento (ex: dia 20)')
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Obrigação Fiscal'
        verbose_name_plural = 'Obrigações Fiscais'
        ordering = ['cliente', 'tipo']

    def __str__(self):
        return f"{self.cliente} - {self.tipo} ({self.periodicidade})"


class LembreteFiscal(models.Model):
    obrigacao = models.ForeignKey(ObrigacaoFiscal, on_delete=models.CASCADE, related_name='lembretes')
    data_vencimento = models.DateField()
    aviso_dias_antecedencia = models.PositiveSmallIntegerField(default=1, help_text='Dias antes do vencimento para notificar')
    notificado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lembrete Fiscal'
        verbose_name_plural = 'Lembretes Fiscais'
        ordering = ['data_vencimento']
        unique_together = ['obrigacao', 'data_vencimento']

    def __str__(self):
        return f"Lembrete: {self.obrigacao} em {self.data_vencimento} (aviso {self.aviso_dias_antecedencia}d antes)"