from django.core.management.base import BaseCommand
from core.models import Cliente, CustomUser
from documentos.models import Documento
from fiscal.models import ObrigacaoFiscal
from datetime import date

class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstração'

    def handle(self, *args, **options):
        # Cria clientes
        c1, _ = Cliente.objects.get_or_create(
            cnpj='00.000.000/0001-00',
            defaults={'razao_social': 'Empresa Alpha LTDA', 'contato_nome': 'Carlos', 'contato_email': 'carlos@alpha.com'}
        )
        c2, _ = Cliente.objects.get_or_create(
            cnpj='11.111.111/1111-11',
            defaults={'razao_social': 'Beta Comércio S.A.', 'contato_nome': 'Ana', 'contato_email': 'ana@beta.com'}
        )

        # Cria usuário contador
        contador, _ = CustomUser.objects.get_or_create(
            username='contador',
            defaults={'first_name': 'João', 'last_name': 'Contador', 'cargo': 'CONTADOR', 'is_staff': True}
        )
        contador.set_password('senha123')
        contador.save()

        # Cria usuário cliente
        cliente_user, _ = CustomUser.objects.get_or_create(
            username='cliente_alpha',
            defaults={'first_name': 'Carlos', 'last_name': 'Cliente', 'cargo': 'CLIENTE', 'empresa': c1}
        )
        cliente_user.set_password('senha123')
        cliente_user.save()

        # Cria documentos para Alpha
        doc1, _ = Documento.objects.get_or_create(
            titulo='Contrato Social',
            categoria='CONTRATO',
            cliente=c1,
            defaults={'descricao': 'Contrato social consolidado', 'responsavel': contador}
        )
        doc2, _ = Documento.objects.get_or_create(
            titulo='DAS-MEI JAN/2026',
            categoria='FISCAL',
            cliente=c1,
            defaults={'descricao': 'Guia de pagamento', 'responsavel': contador}
        )

        # Obrigações fiscais
        ObrigacaoFiscal.objects.get_or_create(
            cliente=c1, tipo='DAS', periodicidade='MENSAL', data_vencimento_base=date(2026,5,20)
        )
        ObrigacaoFiscal.objects.get_or_create(
            cliente=c1, tipo='DIRF', periodicidade='ANUAL', data_vencimento_base=date(2027,2,28)
        )
        ObrigacaoFiscal.objects.get_or_create(
            cliente=c2, tipo='EFD-ICMS', periodicidade='MENSAL', data_vencimento_base=date(2026,5,15)
        )

        self.stdout.write(self.style.SUCCESS('Dados de demonstração criados com sucesso.'))