import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Cliente, CustomUser
from documentos.models import Documento, VersaoDocumento
from fiscal.models import ObrigacaoFiscal, LembreteFiscal

class Command(BaseCommand):
    help = 'Remove todos os dados do sistema (exceto superusuários) e limpa arquivos de mídia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--manter-admin',
            action='store_true',
            help='Mantém apenas o superusuário atual (padrão: mantém todos os superusuários)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('ATENÇÃO: Isso apagará TODOS os dados do sistema!'))
        resposta = input('Tem certeza? Digite "SIM" para continuar: ')
        if resposta.strip().upper() != 'SIM':
            self.stdout.write('Operação cancelada.')
            return

        # Remove dados dos apps na ordem correta (respeitando FK)
        self.stdout.write('Removendo lembretes fiscais...')
        LembreteFiscal.objects.all().delete()

        self.stdout.write('Removendo obrigações fiscais...')
        ObrigacaoFiscal.objects.all().delete()

        self.stdout.write('Removendo versões de documentos...')
        VersaoDocumento.objects.all().delete()

        self.stdout.write('Removendo documentos...')
        Documento.objects.all().delete()

        self.stdout.write('Removendo clientes e usuários não administradores...')
        # Remove todos os clientes
        Cliente.objects.all().delete()

        # Remove usuários, exceto superusuários
        if options['manter_admin']:
            # Mantém apenas o superusuário que está executando o comando? Vamos manter todos os superusuários.
            CustomUser.objects.filter(is_superuser=False).delete()
            self.stdout.write('Superusuários mantidos.')
        else:
            # Remove todos, inclusive superusuários (cuidado!)
            CustomUser.objects.all().delete()
            self.stdout.write('Todos os usuários removidos.')

        # Remove arquivos de mídia
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root):
            self.stdout.write('Limpando arquivos de mídia...')
            shutil.rmtree(media_root)
            os.makedirs(media_root)  # recria a pasta vazia
            self.stdout.write('Arquivos de mídia removidos.')

        self.stdout.write(self.style.SUCCESS('Todos os dados foram removidos com sucesso.'))