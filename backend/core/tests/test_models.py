from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente


class TipoPlanoModelTest(TestCase):
    def test_tipo_plano_creation(self):
        tipo_plano = TipoPlano.objects.create(
            nome="Plano Básico",
            descricao="Plano básico para iniciantes",
            preco="99.90",
            duracao_dias=30,
            intervalo_atualizacao_treino_dieta=7,
            limite_trocas_exercicios=5,
            limite_trocas_refeicoes=3,
            periodo_trocas_dias=7
        )
        self.assertEqual(tipo_plano.nome, "Plano Básico")
        self.assertEqual(tipo_plano.duracao_dias, 30)
        self.assertFalse(tipo_plano.trocas_ilimitadas)
    
    def test_tipo_plano_str_representation(self):
        tipo_plano = TipoPlano.objects.create(
            nome="Plano Premium",
            descricao="Plano premium",
            preco="199.90"
        )
        self.assertEqual(str(tipo_plano), "Plano Premium")


class ClienteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cliente_test',
            email='cliente@test.com',
            password='testpass123'
        )
        # Obter o perfil criado automaticamente pelos signals
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.tipo_plano = TipoPlano.objects.create(
            nome="Plano Teste",
            descricao="Plano para testes",
            preco="99.90",
            duracao_dias=30,
            limite_trocas_exercicios=5,
            limite_trocas_refeicoes=3
        )
    
    def test_cliente_creation(self):
        cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil,
            tipo_plano=self.tipo_plano
        )
        self.assertEqual(cliente.nome, "Cliente Teste")
        self.assertEqual(cliente.perfil, self.perfil)
        self.assertEqual(cliente.tipo_plano, self.tipo_plano)
        self.assertEqual(cliente.trocas_exercicios_restantes, 5)
        self.assertEqual(cliente.trocas_refeicoes_restantes, 3)
    
    def test_cliente_str_representation(self):
        cliente = Cliente.objects.create(
            nome="João Silva",
            email="joao@test.com",
            perfil=self.perfil
        )
        self.assertEqual(str(cliente), "João Silva")