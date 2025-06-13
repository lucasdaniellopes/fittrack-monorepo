from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente
import uuid


class PerfilModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Obter o perfil criado automaticamente pelos signals
        self.perfil = Perfil.objects.get(usuario=self.user)
    
    def test_perfil_auto_creation(self):
        # Verificar se o perfil foi criado automaticamente
        self.assertEqual(self.perfil.usuario, self.user)
        self.assertEqual(self.perfil.tipo, Perfil.CLIENTE)  # Default é cliente
        self.assertIsNotNone(self.perfil.created_at)
        self.assertIsNotNone(self.perfil.updated_at)
    
    def test_perfil_str_representation(self):
        expected = f"{self.user.username} - {self.perfil.get_tipo_display()}"
        self.assertEqual(str(self.perfil), expected)
    
    def test_perfil_types(self):
        # Testar diferentes tipos de perfil
        tipos = [Perfil.ADMIN, Perfil.NUTRICIONISTA, Perfil.PERSONAL, Perfil.CLIENTE]
        for tipo in tipos:
            self.perfil.tipo = tipo
            self.perfil.save()
            self.assertEqual(self.perfil.tipo, tipo)
    
    def test_perfil_unique_usuario(self):
        # Testar que não podemos criar dois perfis para o mesmo usuário
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Perfil.objects.create(
                usuario=self.user,
                tipo=Perfil.ADMIN
            )


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
    
    def test_tipo_plano_trocas_ilimitadas(self):
        tipo_plano = TipoPlano.objects.create(
            nome="Plano Premium",
            descricao="Plano premium com trocas ilimitadas",
            preco="199.90",
            duracao_dias=30,
            trocas_ilimitadas=True
        )
        self.assertTrue(tipo_plano.trocas_ilimitadas)
    
    def test_tipo_plano_str_representation(self):
        tipo_plano = TipoPlano.objects.create(
            nome="Plano VIP",
            descricao="Plano VIP",
            preco="299.90",
            duracao_dias=30
        )
        self.assertEqual(str(tipo_plano), "Plano VIP")
    
    def test_tipo_plano_defaults(self):
        tipo_plano = TipoPlano.objects.create(
            nome="Plano Teste",
            descricao="Teste",
            preco="50.00",
            duracao_dias=30
        )
        # Verificar valores padrão
        self.assertEqual(tipo_plano.duracao_dias, 30)
        self.assertEqual(tipo_plano.intervalo_atualizacao_treino_dieta, 60)
        self.assertFalse(tipo_plano.trocas_ilimitadas)


class ClienteModelTest(TestCase):
    def setUp(self):
        unique_id = str(uuid.uuid4())[:8]
        self.user = User.objects.create_user(
            username=f'cliente_test_{unique_id}',
            email=f'cliente_{unique_id}@test.com',
            password='testpass123'
        )
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
        # Create unique user for this test
        unique_id = str(uuid.uuid4())[:8]
        user = User.objects.create_user(
            username=f'cliente_creation_test_{unique_id}',
            email=f'cliente_creation_{unique_id}@test.com',
            password='testpass123'
        )
        perfil = Perfil.objects.get(usuario=user)
        
        cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email=f"cliente_creation_{unique_id}@test.com",
            perfil=perfil,
            tipo_plano=self.tipo_plano
        )
        self.assertEqual(cliente.nome, "Cliente Teste")
        self.assertEqual(cliente.perfil, perfil)
        self.assertEqual(cliente.tipo_plano, self.tipo_plano)
        self.assertEqual(cliente.trocas_exercicios_restantes, 5)
        self.assertEqual(cliente.trocas_refeicoes_restantes, 3)
    
    def test_cliente_str_representation(self):
        # Create unique user for this test
        unique_id = str(uuid.uuid4())[:8]
        user = User.objects.create_user(
            username=f'cliente_str_test_{unique_id}',
            email=f'cliente_str_{unique_id}@test.com',
            password='testpass123'
        )
        perfil = Perfil.objects.get(usuario=user)
        
        cliente = Cliente.objects.create(
            nome="João Silva",
            email=f"cliente_str_{unique_id}@test.com",
            perfil=perfil
        )
        self.assertEqual(str(cliente), "João Silva")
    
    def test_cliente_without_tipo_plano(self):
        # Create unique user for this test
        unique_id = str(uuid.uuid4())[:8]
        user = User.objects.create_user(
            username=f'cliente_sem_plano_test_{unique_id}',
            email=f'sem_plano_{unique_id}@test.com',
            password='testpass123'
        )
        perfil = Perfil.objects.get(usuario=user)
        
        cliente = Cliente.objects.create(
            nome="Cliente Sem Plano",
            email=f"sem_plano_{unique_id}@test.com",
            perfil=perfil
        )
        # Sem tipo de plano, deve ter 0 trocas
        self.assertEqual(cliente.trocas_exercicios_restantes, 0)
        self.assertEqual(cliente.trocas_refeicoes_restantes, 0)
    
    def test_cliente_soft_delete(self):
        # Create unique user for this test
        unique_id = str(uuid.uuid4())[:8]
        user = User.objects.create_user(
            username=f'cliente_delete_test_{unique_id}',
            email=f'deletar_{unique_id}@test.com',
            password='testpass123'
        )
        perfil = Perfil.objects.get(usuario=user)
        
        cliente = Cliente.objects.create(
            nome="Cliente para Deletar",
            email=f"deletar_{unique_id}@test.com",
            perfil=perfil
        )
        
        # Soft delete
        from django.utils import timezone
        cliente.deleted_at = timezone.now()
        cliente.save()
        
        self.assertIsNotNone(cliente.deleted_at)
    
    def test_cliente_update_trocas(self):
        # Create unique user for this test
        unique_id = str(uuid.uuid4())[:8]
        user = User.objects.create_user(
            username=f'cliente_trocas_test_{unique_id}',
            email=f'trocas_{unique_id}@test.com',
            password='testpass123'
        )
        perfil = Perfil.objects.get(usuario=user)
        
        cliente = Cliente.objects.create(
            nome="Cliente Trocas",
            email=f"trocas_{unique_id}@test.com",
            perfil=perfil,
            tipo_plano=self.tipo_plano
        )
        
        # Diminuir trocas restantes
        cliente.trocas_exercicios_restantes = 3
        cliente.trocas_refeicoes_restantes = 1
        cliente.save()
        
        cliente.refresh_from_db()
        self.assertEqual(cliente.trocas_exercicios_restantes, 3)
        self.assertEqual(cliente.trocas_refeicoes_restantes, 1)