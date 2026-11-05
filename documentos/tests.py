from django.test import TestCase
from core.models import Cliente, CustomUser
from documentos.models import Documento

class SistemaGestaoTests(TestCase):
    def setUp(self):
        # Configuração inicial: cria um cliente e um usuário para os testes
        self.cliente_teste = Cliente.objects.create(
            razao_social="Empresa Teste UNIVESP",
            cnpj="11.222.333/0001-44",
            ativo=True
        )
        self.usuario_teste = CustomUser.objects.create_user(
            username="contador_teste",
            password="senha_segura_123",
            cargo="CONTADOR"
        )
        self.documento_teste = Documento.objects.create(
            titulo="Guia DAS Maio",
            categoria="FISCAL",
            cliente=self.cliente_teste,
            arquivo_atual="fake_path/guia.pdf",
            responsavel=self.usuario_teste
        )

    def test_criacao_cliente(self):
        """Verifica se o cliente foi criado corretamente no banco"""
        cliente = Cliente.objects.get(cnpj="11.222.333/0001-44")
        self.assertEqual(cliente.razao_social, "Empresa Teste UNIVESP")
        self.assertTrue(cliente.ativo)

    def test_relacionamento_documento_cliente(self):
        """Verifica se o documento pertence ao cliente correto (Integridade Referencial)"""
        self.assertEqual(self.documento_teste.cliente, self.cliente_teste)
        self.assertEqual(self.documento_teste.responsavel.username, "contador_teste")