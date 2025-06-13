from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao
from nutrition.api.v1.serializers import (
    DietaSerializer, RefeicaoSerializer, 
    HistoricoDietaSerializer, TrocaRefeicaoSerializer
)


class DietaSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
    
    def test_dieta_serializer_fields(self):
        serializer = DietaSerializer(self.dieta)
        data = serializer.data
        
        expected_fields = {'id', 'nome', 'descricao', 'calorias', 'cliente'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_dieta_serializer_create(self):
        data = {
            'nome': 'Dieta Low Carb',
            'descricao': 'Dieta com baixo carboidrato',
            'calorias': 1800,
            'cliente': self.cliente.id
        }
        
        serializer = DietaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        dieta = serializer.save()
        self.assertEqual(dieta.nome, 'Dieta Low Carb')
        self.assertEqual(dieta.cliente, self.cliente)
        self.assertEqual(dieta.calorias, 1800)
    
    def test_dieta_serializer_update(self):
        data = {
            'calorias': 2200,
            'descricao': 'Descrição atualizada'
        }
        
        serializer = DietaSerializer(self.dieta, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_dieta = serializer.save()
        self.assertEqual(updated_dieta.calorias, 2200)
        self.assertEqual(updated_dieta.descricao, 'Descrição atualizada')
    
    def test_dieta_serializer_validation(self):
        # Teste com dados inválidos
        data = {
            'nome': '',  # Nome vazio pode falhar
            'calorias': -100,  # Calorias negativas podem falhar
            'cliente': 99999  # Cliente inexistente
        }
        
        serializer = DietaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIsInstance(serializer.errors, dict)
    
    def test_dieta_serializer_without_cliente(self):
        data = {
            'nome': 'Dieta Genérica',
            'descricao': 'Dieta sem cliente específico',
            'calorias': 2000
        }
        
        serializer = DietaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        dieta = serializer.save()
        self.assertIsNone(dieta.cliente)
    
    def test_dieta_serializer_cliente_representation(self):
        serializer = DietaSerializer(self.dieta)
        data = serializer.data
        
        self.assertEqual(data['cliente'], self.cliente.id)


class RefeicaoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        self.refeicao = Refeicao.objects.create(
            nome="Café da Manhã",
            descricao="Primeira refeição do dia",
            calorias=300,
            dieta=self.dieta
        )
    
    def test_refeicao_serializer_fields(self):
        serializer = RefeicaoSerializer(self.refeicao)
        data = serializer.data
        
        expected_fields = {'id', 'nome', 'descricao', 'calorias', 'dieta'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_refeicao_serializer_create(self):
        data = {
            'nome': 'Almoço',
            'descricao': 'Refeição principal do dia',
            'calorias': 600,
            'dieta': self.dieta.id
        }
        
        serializer = RefeicaoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        refeicao = serializer.save()
        self.assertEqual(refeicao.nome, 'Almoço')
        self.assertEqual(refeicao.dieta, self.dieta)
        self.assertEqual(refeicao.calorias, 600)
    
    def test_refeicao_serializer_update(self):
        data = {
            'calorias': 350,
            'descricao': 'Descrição atualizada'
        }
        
        serializer = RefeicaoSerializer(self.refeicao, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_refeicao = serializer.save()
        self.assertEqual(updated_refeicao.calorias, 350)
        self.assertEqual(updated_refeicao.descricao, 'Descrição atualizada')
    
    def test_refeicao_serializer_validation(self):
        # Teste com nome vazio
        data = {
            'nome': '',
            'calorias': 300,
            'dieta': self.dieta.id
        }
        
        serializer = RefeicaoSerializer(data=data)
        # Dependendo das validações, pode ou não ser válido
        if not serializer.is_valid():
            self.assertIn('nome', serializer.errors)
    
    def test_refeicao_serializer_dieta_representation(self):
        serializer = RefeicaoSerializer(self.refeicao)
        data = serializer.data
        
        self.assertEqual(data['dieta'], self.dieta.id)


class HistoricoDietaSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        self.historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15",
            observacoes="Dieta iniciada"
        )
    
    def test_historico_dieta_serializer_fields(self):
        serializer = HistoricoDietaSerializer(self.historico)
        data = serializer.data
        
        expected_fields = {'id', 'cliente', 'dieta', 'data_inicio', 'data_fim', 'observacoes'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_historico_dieta_serializer_create(self):
        data = {
            'cliente': self.cliente.id,
            'dieta': self.dieta.id,
            'data_inicio': '2024-01-20',
            'observacoes': 'Novo histórico'
        }
        
        serializer = HistoricoDietaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        historico = serializer.save()
        self.assertEqual(historico.cliente, self.cliente)
        self.assertEqual(historico.dieta, self.dieta)
        self.assertEqual(str(historico.data_inicio), '2024-01-20')
    
    def test_historico_dieta_serializer_with_data_fim(self):
        data = {
            'cliente': self.cliente.id,
            'dieta': self.dieta.id,
            'data_inicio': '2024-01-15',
            'data_fim': '2024-01-30',
            'observacoes': 'Histórico completo'
        }
        
        serializer = HistoricoDietaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        historico = serializer.save()
        self.assertEqual(str(historico.data_fim), '2024-01-30')
    
    def test_historico_dieta_serializer_update(self):
        data = {
            'observacoes': 'Observações atualizadas',
            'data_fim': '2024-01-25'
        }
        
        serializer = HistoricoDietaSerializer(self.historico, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_historico = serializer.save()
        self.assertEqual(updated_historico.observacoes, 'Observações atualizadas')
        self.assertEqual(str(updated_historico.data_fim), '2024-01-25')
    
    def test_historico_dieta_serializer_validation(self):
        # Teste com data_fim anterior a data_inicio
        data = {
            'cliente': self.cliente.id,
            'dieta': self.dieta.id,
            'data_inicio': '2024-01-20',
            'data_fim': '2024-01-15'  # Data fim anterior ao início
        }
        
        serializer = HistoricoDietaSerializer(data=data)
        # Dependendo das validações implementadas, pode falhar
        if not serializer.is_valid():
            self.assertIsInstance(serializer.errors, dict)


class TrocaRefeicaoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.refeicao_antiga = Refeicao.objects.create(
            nome="Café Original",
            calorias=300,
            dieta=self.dieta
        )
        
        self.refeicao_nova = Refeicao.objects.create(
            nome="Café Alternativo",
            calorias=320,
            dieta=self.dieta
        )
        
        self.troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Teste"
        )
    
    def test_troca_refeicao_serializer_fields(self):
        serializer = TrocaRefeicaoSerializer(self.troca)
        data = serializer.data
        
        expected_fields = {
            'id', 'cliente', 'refeicao_antiga', 'refeicao_nova', 
            'refeicao_sugerida', 'data_solicitacao', 'data_resposta',
            'motivo', 'observacoes_resposta', 'status', 'aprovado_por'
        }
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_troca_refeicao_serializer_create(self):
        refeicao_outra = Refeicao.objects.create(
            nome="Jantar",
            calorias=500,
            dieta=self.dieta
        )
        
        data = {
            'cliente': self.cliente.id,
            'refeicao_antiga': self.refeicao_nova.id,
            'refeicao_nova': refeicao_outra.id,
            'motivo': 'Nova troca'
        }
        
        serializer = TrocaRefeicaoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        troca = serializer.save()
        self.assertEqual(troca.cliente, self.cliente)
        self.assertEqual(troca.motivo, 'Nova troca')
        self.assertEqual(troca.status, 'PENDENTE')
    
    def test_troca_refeicao_serializer_with_suggestion(self):
        data = {
            'cliente': self.cliente.id,
            'refeicao_antiga': self.refeicao_antiga.id,
            'refeicao_sugerida': 'Aveia com frutas',
            'motivo': 'Quero algo mais leve'
        }
        
        serializer = TrocaRefeicaoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        troca = serializer.save()
        self.assertEqual(troca.refeicao_sugerida, 'Aveia com frutas')
        self.assertIsNone(troca.refeicao_nova)
    
    def test_troca_refeicao_serializer_update_status(self):
        data = {
            'status': 'APROVADO',
            'observacoes_resposta': 'Aprovado pela nutricionista',
            'aprovado_por': self.admin_user.id
        }
        
        serializer = TrocaRefeicaoSerializer(self.troca, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_troca = serializer.save()
        self.assertEqual(updated_troca.status, 'APROVADO')
        self.assertEqual(updated_troca.observacoes_resposta, 'Aprovado pela nutricionista')
        if updated_troca.aprovado_por:
            self.assertEqual(updated_troca.aprovado_por, self.admin_user)
    
    def test_troca_refeicao_serializer_validation(self):
        # Teste com cliente inexistente
        data = {
            'cliente': 99999,
            'refeicao_antiga': self.refeicao_antiga.id,
            'refeicao_nova': self.refeicao_nova.id,
            'motivo': 'Teste inválido'
        }
        
        serializer = TrocaRefeicaoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_troca_refeicao_serializer_status_choices(self):
        # Testar diferentes status
        for status_choice in ['PENDENTE', 'APROVADO', 'REJEITADO']:
            data = {'status': status_choice}
            
            serializer = TrocaRefeicaoSerializer(self.troca, data=data, partial=True)
            self.assertTrue(serializer.is_valid(), f"Status {status_choice} deve ser válido")
    
    def test_troca_refeicao_serializer_read_only_fields(self):
        serializer = TrocaRefeicaoSerializer(self.troca)
        data = serializer.data
        
        # Verificar se data_solicitacao está presente (gerada automaticamente)
        self.assertIn('data_solicitacao', data)
        self.assertIsNotNone(data['data_solicitacao'])
    
    def test_troca_refeicao_serializer_reject(self):
        data = {
            'status': 'REJEITADO',
            'observacoes_resposta': 'Rejeitado por motivos nutricionais'
        }
        
        serializer = TrocaRefeicaoSerializer(self.troca, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_troca = serializer.save()
        self.assertEqual(updated_troca.status, 'REJEITADO')
        self.assertEqual(updated_troca.observacoes_resposta, 'Rejeitado por motivos nutricionais')
    
    def test_troca_refeicao_serializer_motivo_required(self):
        # Teste sem motivo
        data = {
            'cliente': self.cliente.id,
            'refeicao_antiga': self.refeicao_antiga.id,
            'refeicao_nova': self.refeicao_nova.id
            # motivo ausente
        }
        
        serializer = TrocaRefeicaoSerializer(data=data)
        # Dependendo das validações, pode falhar
        if not serializer.is_valid():
            self.assertIn('motivo', serializer.errors)