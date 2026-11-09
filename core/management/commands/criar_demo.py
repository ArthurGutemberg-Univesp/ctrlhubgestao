from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import os

from core.models import Cliente, CustomUser
from documentos.models import Documento, VersaoDocumento
from fiscal.models import ObrigacaoFiscal, LembreteFiscal
from fiscal.utils import calcular_proximas_datas


class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstração'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de demonstração...')

        # --- Clientes ---
        cliente1, _ = Cliente.objects.get_or_create(
            cnpj='12.345.678/0001-90',
            defaults={
                'razao_social': 'Comércio ABC Ltda',
                'contato_nome': 'Carlos Silva',
                'contato_email': 'carlos@abc.com',
                'ativo': True,
            }
        )
        cliente2, _ = Cliente.objects.get_or_create(
            cnpj='98.765.432/0001-10',
            defaults={
                'razao_social': 'Indústria XYZ S.A.',
                'contato_nome': 'Ana Souza',
                'contato_email': 'ana@xyz.com',
                'ativo': True,
            }
        )
        cliente3, _ = Cliente.objects.get_or_create(
            cnpj='11.222.333/0001-44',
            defaults={
                'razao_social': 'Serviços Rápidos ME',
                'contato_nome': 'Roberto Lima',
                'contato_email': 'roberto@servicosrapidos.com',
                'ativo': True,
            }
        )

        # --- Usuários ---
        # Administrador (já deve existir; se não, cria)
        admin, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ctrlhub.com',
                'cargo': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()

        # Contador
        contador, created = CustomUser.objects.get_or_create(
            username='joao.contador',
            defaults={
                'first_name': 'João',
                'last_name': 'Contador',
                'email': 'joao@ctrlhub.com',
                'cargo': 'CONTADOR',
                'is_staff': True,
            }
        )
        if created:
            contador.set_password('teste123')
            contador.save()

        # Cliente (usuário da empresa ABC)
        cliente_user, created = CustomUser.objects.get_or_create(
            username='empresa_abc',
            defaults={
                'first_name': 'Carlos',
                'last_name': 'Silva',
                'email': 'carlos@abc.com',
                'cargo': 'CLIENTE',
                'empresa': cliente1,
            }
        )
        if created:
            cliente_user.set_password('teste123')
            cliente_user.save()

        # --- Documentos de demonstração ---
        # Cria arquivos fake se não existirem
        media_root = 'media/documentos/2026/05'
        os.makedirs(media_root, exist_ok=True)

        # Lista de documentos fictícios
        docs_info = [
            {'titulo': 'Nota Fiscal Eletrônica 001/2026', 'categoria': 'FISCAL', 'cliente': cliente1},
            {'titulo': 'Contrato Social Consolidado', 'categoria': 'CONTRATO', 'cliente': cliente1},
            {'titulo': 'Folha de Pagamento Maio 2026', 'categoria': 'FOLHA', 'cliente': cliente1},
            {'titulo': 'Nota Fiscal de Serviço 050/2026', 'categoria': 'FISCAL', 'cliente': cliente2},
            {'titulo': 'Guia de Recolhimento do FGTS', 'categoria': 'FISCAL', 'cliente': cliente2},
            {'titulo': 'Contrato de Prestação de Serviços', 'categoria': 'CONTRATO', 'cliente': cliente2},
            {'titulo': 'Folha de Pagamento Abril 2026', 'categoria': 'FOLHA', 'cliente': cliente3},
            {'titulo': 'Declaração de Imposto de Renda', 'categoria': 'FISCAL', 'cliente': cliente3},
            {'titulo': 'Alvará de Funcionamento 2026', 'categoria': 'OUTROS', 'cliente': cliente3},
        ]

        for info in docs_info:
            # Cria um arquivo fake de texto para simular o documento
            filename = f"{info['titulo'].replace(' ', '_').replace('/', '-')}.txt"
            filepath = os.path.join(media_root, filename)
            with open(filepath, 'w') as f:
                f.write(f"Documento simulado: {info['titulo']}\n")
                f.write(f"Cliente: {info['cliente'].razao_social}\n")
                f.write("Conteúdo fictício para demonstração.\n")

            # Cria o registro no banco (se não existir mesmo título)
            doc, created = Documento.objects.get_or_create(
                titulo=info['titulo'],
                cliente=info['cliente'],
                defaults={
                    'descricao': f'Demo: {info["titulo"]}',
                    'categoria': info['categoria'],
                    'arquivo_atual': f'documentos/2026/05/{filename}',
                    'versao_atual': 1,
                    'responsavel': contador,
                }
            )
            if created:
                # Cria uma versão inicial
                VersaoDocumento.objects.create(
                    documento=doc,
                    arquivo=f'documentos/2026/05/{filename}',
                    numero_versao=1,
                    usuario=contador,
                    comentario='Versão inicial de demonstração.'
                )

        # --- Obrigações Fiscais de demonstração ---
        hoje = date.today()
        obrigacoes_info = [
            {'cliente': cliente1, 'tipo': 'DAS - Simples Nacional', 'periodicidade': 'MENSAL', 'data_vencimento_base': hoje.replace(day=20), 'descricao': 'Pagamento unificado de impostos'},
            {'cliente': cliente1, 'tipo': 'DIRF', 'periodicidade': 'ANUAL', 'data_vencimento_base': hoje.replace(month=2, day=28), 'descricao': 'Declaração de Imposto de Renda Retido na Fonte'},
            {'cliente': cliente2, 'tipo': 'EFD-ICMS', 'periodicidade': 'MENSAL', 'data_vencimento_base': hoje.replace(day=15), 'descricao': 'Escrituração Fiscal Digital do ICMS'},
            {'cliente': cliente2, 'tipo': 'PIS/COFINS', 'periodicidade': 'MENSAL', 'data_vencimento_base': hoje.replace(day=25), 'descricao': 'Contribuição para PIS e COFINS'},
            {'cliente': cliente3, 'tipo': 'ISS', 'periodicidade': 'MENSAL', 'data_vencimento_base': hoje.replace(day=10), 'descricao': 'Imposto Sobre Serviços'},
            {'cliente': cliente3, 'tipo': 'DCTF', 'periodicidade': 'MENSAL', 'data_vencimento_base': hoje.replace(day=15), 'descricao': 'Declaração de Débitos e Créditos Tributários Federais'},
        ]

        for ob_info in obrigacoes_info:
            ob, created = ObrigacaoFiscal.objects.get_or_create(
                cliente=ob_info['cliente'],
                tipo=ob_info['tipo'],
                defaults={
                    'periodicidade': ob_info['periodicidade'],
                    'data_vencimento_base': ob_info['data_vencimento_base'],
                    'descricao': ob_info['descricao'],
                    'ativo': True,
                }
            )
            # Gera lembretes para os próximos vencimentos
            if created:
                datas = calcular_proximas_datas(ob.data_vencimento_base, ob.periodicidade, meses_adiante=2)
                for d in datas:
                    LembreteFiscal.objects.get_or_create(
                        obrigacao=ob,
                        data_vencimento=d,
                        defaults={'aviso_dias_antecedencia': 3, 'notificado': False}
                    )

        self.stdout.write(self.style.SUCCESS('Dados de demonstração criados com sucesso!'))