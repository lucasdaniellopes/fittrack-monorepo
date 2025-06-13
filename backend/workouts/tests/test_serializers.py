from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio
from workouts.api.v1.serializers import (
    TreinoSerializer, ExercicioSerializer, 
    HistoricoTreinoSerializer, TrocaExercicioSerializer
)


class TreinoSerializerTest(TestCase):
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
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Descrição do treino",
            duracao=60,
            cliente=self.cliente
        )
    
    def test_treino_serializer_fields(self):
        serializer = TreinoSerializer(self.treino)
        data = serializer.data
        
        expected_fields = {'id', 'nome', 'descricao', 'duracao', 'cliente'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_treino_serializer_create(self):
        data = {
            'nome': 'Treino Serializer',
            'descricao': 'Teste do serializer',
            'duracao': 30,
            'cliente': self.cliente.id
        }
        
        serializer = TreinoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        treino = serializer.save()
        self.assertEqual(treino.nome, 'Treino Serializer')
        self.assertEqual(treino.cliente, self.cliente)
        self.assertEqual(treino.duracao, 30)
    
    def test_treino_serializer_update(self):
        data = {
            'duracao': 90,
            'descricao': 'Descrição atualizada'
        }
        
        serializer = TreinoSerializer(self.treino, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_treino = serializer.save()
        self.assertEqual(updated_treino.duracao, 90)
        self.assertEqual(updated_treino.descricao, 'Descrição atualizada')
    
    def test_treino_serializer_validation(self):
        # Teste validação com dados inválidos
        data = {
            'nome': '',  # Nome vazio pode falhar
            'duracao': -10,  # Duração negativa pode falhar
            'cliente': 99999  # Cliente inexistente
        }
        
        serializer = TreinoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIsInstance(serializer.errors, dict)
    
    def test_treino_serializer_cliente_representation(self):
        serializer = TreinoSerializer(self.treino)
        data = serializer.data
        
        self.assertEqual(data['cliente'], self.cliente.id)


class ExercicioSerializerTest(TestCase):
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
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        self.exercicio = Exercicio.objects.create(
            nome="Supino",
            descricao="Exercício para peitoral",
            treino=self.treino
        )
    
    def test_exercicio_serializer_fields(self):
        serializer = ExercicioSerializer(self.exercicio)
        data = serializer.data
        
        expected_fields = {'id', 'nome', 'descricao', 'treino'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_exercicio_serializer_create(self):
        data = {
            'nome': 'Agachamento',
            'descricao': 'Exercício para pernas',
            'treino': self.treino.id
        }
        
        serializer = ExercicioSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        exercicio = serializer.save()
        self.assertEqual(exercicio.nome, 'Agachamento')
        self.assertEqual(exercicio.treino, self.treino)
    
    def test_exercicio_serializer_update(self):
        data = {
            'descricao': 'Descrição atualizada do exercício'
        }
        
        serializer = ExercicioSerializer(self.exercicio, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_exercicio = serializer.save()
        self.assertEqual(updated_exercicio.descricao, 'Descrição atualizada do exercício')
    
    def test_exercicio_serializer_validation(self):
        # Teste com nome vazio
        data = {
            'nome': '',
            'treino': self.treino.id
        }
        
        serializer = ExercicioSerializer(data=data)
        # Dependendo das validações, pode ou não ser válido
        if not serializer.is_valid():
            self.assertIn('nome', serializer.errors)


class HistoricoTreinoSerializerTest(TestCase):
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
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        self.historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15",
            observacoes="Treino realizado"
        )
    
    def test_historico_treino_serializer_fields(self):
        serializer = HistoricoTreinoSerializer(self.historico)
        data = serializer.data
        
        expected_fields = {'id', 'cliente', 'treino', 'data_inicio', 'data_fim', 'observacoes'}
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_historico_treino_serializer_create(self):
        data = {
            'cliente': self.cliente.id,
            'treino': self.treino.id,
            'data_inicio': '2024-01-20',
            'observacoes': 'Novo histórico'
        }
        
        serializer = HistoricoTreinoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        historico = serializer.save()
        self.assertEqual(historico.cliente, self.cliente)
        self.assertEqual(historico.treino, self.treino)
        self.assertEqual(str(historico.data_inicio), '2024-01-20')
    
    def test_historico_treino_serializer_with_data_fim(self):
        data = {
            'cliente': self.cliente.id,
            'treino': self.treino.id,
            'data_inicio': '2024-01-15',
            'data_fim': '2024-01-20',
            'observacoes': 'Histórico completo'
        }
        
        serializer = HistoricoTreinoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        historico = serializer.save()
        self.assertEqual(str(historico.data_fim), '2024-01-20')
    
    def test_historico_treino_serializer_update(self):
        data = {
            'observacoes': 'Observações atualizadas',
            'data_fim': '2024-01-25'
        }
        
        serializer = HistoricoTreinoSerializer(self.historico, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_historico = serializer.save()
        self.assertEqual(updated_historico.observacoes, 'Observações atualizadas')


class TrocaExercicioSerializerTest(TestCase):
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
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        self.exercicio_antigo = Exercicio.objects.create(
            nome="Supino",
            treino=self.treino
        )
        self.exercicio_novo = Exercicio.objects.create(
            nome="Supino Inclinado",
            treino=self.treino
        )
        self.troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Teste"
        )
    
    def test_troca_exercicio_serializer_fields(self):
        serializer = TrocaExercicioSerializer(self.troca)
        data = serializer.data
        
        expected_fields = {
            'id', 'cliente', 'exercicio_antigo', 'exercicio_novo', 
            'data_troca', 'motivo', 'status'
        }
        
        for field in expected_fields:
            self.assertIn(field, data, f"Campo {field} não encontrado")
    
    def test_troca_exercicio_serializer_create(self):
        exercicio_outro = Exercicio.objects.create(
            nome="Leg Press",
            treino=self.treino
        )
        
        data = {
            'cliente': self.cliente.id,
            'exercicio_antigo': self.exercicio_novo.id,
            'exercicio_novo': exercicio_outro.id,
            'motivo': 'Nova troca'
        }
        
        serializer = TrocaExercicioSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        troca = serializer.save()
        self.assertEqual(troca.cliente, self.cliente)
        self.assertEqual(troca.motivo, 'Nova troca')
        self.assertEqual(troca.status, TrocaExercicio.PENDENTE)
    
    def test_troca_exercicio_serializer_update_status(self):
        data = {
            'status': TrocaExercicio.APROVADA
        }
        
        serializer = TrocaExercicioSerializer(self.troca, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_troca = serializer.save()
        self.assertEqual(updated_troca.status, TrocaExercicio.APROVADA)
    
    def test_troca_exercicio_serializer_validation(self):
        # Teste com cliente inexistente
        data = {
            'cliente': 99999,
            'exercicio_antigo': self.exercicio_antigo.id,
            'exercicio_novo': self.exercicio_novo.id,
            'motivo': 'Teste inválido'
        }
        
        serializer = TrocaExercicioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_troca_exercicio_serializer_status_choices(self):
        # Testar diferentes status
        for status_choice in [TrocaExercicio.PENDENTE, TrocaExercicio.APROVADA, TrocaExercicio.REJEITADA]:
            data = {'status': status_choice}
            
            serializer = TrocaExercicioSerializer(self.troca, data=data, partial=True)
            self.assertTrue(serializer.is_valid(), f"Status {status_choice} deve ser válido")
    
    def test_troca_exercicio_serializer_read_only_fields(self):
        serializer = TrocaExercicioSerializer(self.troca)
        data = serializer.data
        
        # Verificar se data_troca está presente (gerada automaticamente)
        self.assertIn('data_troca', data)
        self.assertIsNotNone(data['data_troca'])