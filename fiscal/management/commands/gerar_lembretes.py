from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import date, timedelta
from fiscal.models import ObrigacaoFiscal, LembreteFiscal
from fiscal.utils import calcular_proximas_datas

class Command(BaseCommand):
    help = 'Gera lembretes para obrigações fiscais e envia e-mails de aviso'

    def handle(self, *args, **options):
        hoje = timezone.localdate()
        obrigacoes_ativas = ObrigacaoFiscal.objects.filter(ativo=True)

        for obrigacao in obrigacoes_ativas:
            # Calcula as próximas datas (próximos 3 meses)
            datas_futuras = calcular_proximas_datas(
                obrigacao.data_vencimento_base,
                obrigacao.periodicidade,
                meses_adiante=3
            )
            for data_venc in datas_futuras:
                # Verifica se o vencimento está dentro dos próximos 5 dias
                diff = (data_venc - hoje).days
                if 0 <= diff <= 5:
                    # Cria o lembrete se não existir
                    lembrete, created = LembreteFiscal.objects.get_or_create(
                        obrigacao=obrigacao,
                        data_vencimento=data_venc,
                        defaults={'aviso_dias_antecedencia': 3}  # padrão
                    )
                    if created:
                        # Monta e-mail para os contadores vinculados ao cliente
                        contadores = obrigacao.cliente.usuarios.filter(cargo='CONTADOR')
                        for contador in contadores:
                            send_mail(
                                subject=f'Lembrete Fiscal: {obrigacao.tipo}',
                                message=f'Prezado(a) {contador.first_name},\n\n'
                                        f'O vencimento {obrigacao.tipo} da empresa {obrigacao.cliente.razao_social} '
                                        f'ocorrerá em {data_venc.strftime("%d/%m/%Y")}.',
                                from_email='sistema@ctrlhub.com.br',
                                recipient_list=[contador.email],
                            )
                            self.stdout.write(self.style.SUCCESS(
                                f'E-mail enviado para {contador.email}'
                            ))
                        lembrete.notificado = True
                        lembrete.save()
        self.stdout.write(self.style.SUCCESS('Verificação de lembretes concluída.'))