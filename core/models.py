from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Cliente(models.Model):
    """
    Empresa cliente da contabilidade.
    """
    razao_social = models.CharField("Razão Social", max_length=200)
    cnpj = models.CharField(
        "CNPJ",
        max_length=18,
        unique=True,
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                                    message='CNPJ no formato XX.XXX.XXX/XXXX-XX')]
    )
    contato_nome = models.CharField("Nome do contato", max_length=100, blank=True)
    contato_email = models.EmailField("E-mail do contato", blank=True)
    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['razao_social']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"


class CustomUser(AbstractUser):
    """
    Usuário do sistema com cargo e vínculo opcional a um cliente.
    """
    CARGO_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CONTADOR', 'Contador'),
        ('CLIENTE', 'Cliente'),
    ]
    cargo = models.CharField(max_length=10, choices=CARGO_CHOICES, default='CLIENTE')
    empresa = models.ForeignKey(
        Cliente,
        verbose_name="Empresa vinculada",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_cargo_display()})"