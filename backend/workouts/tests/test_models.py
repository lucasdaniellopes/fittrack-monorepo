from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente, TipoPlano
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio


class TreinoModelTest(TestCase):
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
    
    def test_treino_creation(self):
        treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Descrição do treino",
            duracao=60,
            cliente=self.cliente
        )
        self.assertEqual(treino.nome, "Treino Teste")
        self.assertEqual(treino.duracao, 60)
        self.assertEqual(treino.cliente, self.cliente)
        self.assertIsNotNone(treino.created_at)
    
    def test_treino_str_representation(self):
        treino = Treino.objects.create(
            nome="Treino Push",
            descricao="Treino de empurrar",
            duracao=45,
            cliente=self.cliente
        )
        self.assertEqual(str(treino), "Treino Push")
    
    def test_treino_default_values(self):
        treino = Treino.objects.create(
            nome="Treino Mínimo",
            cliente=self.cliente
        )
        # Verificar valores padrão se houver
        self.assertEqual(treino.nome, "Treino Mínimo")
        self.assertEqual(treino.cliente, self.cliente)
    
    def test_treino_soft_delete(self):
        treino = Treino.objects.create(
            nome="Treino para Deletar",
            descricao="Será deletado",
            duracao=30,
            cliente=self.cliente
        )
        
        # Soft delete
        from django.utils import timezone
        treino.deleted_at = timezone.now()
        treino.save()
        
        self.assertIsNotNone(treino.deleted_at)


class ExercicioModelTest(TestCase):
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
    
    def test_exercicio_creation(self):
        exercicio = Exercicio.objects.create(
            nome="Supino",
            descricao="Exercício para peitoral",
            treino=self.treino
        )
        self.assertEqual(exercicio.nome, "Supino")
        self.assertEqual(exercicio.treino, self.treino)
        self.assertIsNotNone(exercicio.created_at)
    
    def test_exercicio_str_representation(self):
        exercicio = Exercicio.objects.create(
            nome="Agachamento",
            descricao="Exercício para pernas",
            treino=self.treino
        )
        self.assertEqual(str(exercicio), "Agachamento")
    
    def test_exercicio_without_description(self):
        exercicio = Exercicio.objects.create(
            nome="Flexão",
            treino=self.treino
        )
        self.assertEqual(exercicio.nome, "Flexão")
        self.assertEqual(exercicio.treino, self.treino)
    
    def test_multiple_exercicios_per_treino(self):
        exercicio1 = Exercicio.objects.create(
            nome="Supino",
            descricao="Exercício 1",
            treino=self.treino
        )
        exercicio2 = Exercicio.objects.create(
            nome="Agachamento",
            descricao="Exercício 2",
            treino=self.treino
        )
        
        exercicios_do_treino = Exercicio.objects.filter(treino=self.treino)
        self.assertEqual(exercicios_do_treino.count(), 2)
        self.assertIn(exercicio1, exercicios_do_treino)
        self.assertIn(exercicio2, exercicios_do_treino)


class HistoricoTreinoModelTest(TestCase):
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
    
    def test_historico_treino_creation(self):
        historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15",
            observacoes="Treino realizado com sucesso"
        )
        self.assertEqual(historico.cliente, self.cliente)
        self.assertEqual(historico.treino, self.treino)
        self.assertEqual(str(historico.data_inicio), "2024-01-15")
        self.assertEqual(historico.observacoes, "Treino realizado com sucesso")
    
    def test_historico_treino_str_representation(self):
        historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15"
        )
        expected = f"{self.cliente.nome} - {self.treino.nome} - 2024-01-15"
        self.assertEqual(str(historico), expected)
    
    def test_historico_treino_with_data_fim(self):
        historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15",
            data_fim="2024-01-20"
        )
        self.assertEqual(str(historico.data_inicio), "2024-01-15")
        self.assertEqual(str(historico.data_fim), "2024-01-20")
    
    def test_historico_treino_without_observacoes(self):
        historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15"
        )
        self.assertIsNone(historico.observacoes)
    
    def test_multiple_historicos_per_cliente(self):
        historico1 = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15"
        )
        
        treino2 = Treino.objects.create(
            nome="Treino 2",
            cliente=self.cliente
        )
        
        historico2 = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=treino2,
            data_inicio="2024-01-16"
        )
        
        historicos_do_cliente = HistoricoTreino.objects.filter(cliente=self.cliente)
        self.assertEqual(historicos_do_cliente.count(), 2)


class TrocaExercicioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.tipo_plano = TipoPlano.objects.create(
            nome="Plano Teste",
            descricao="Plano para testes",
            preco="99.90",
            duracao_dias=30,
            limite_trocas_exercicios=5
        )
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil,
            tipo_plano=self.tipo_plano
        )
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Descrição do treino",
            duracao=60,
            cliente=self.cliente
        )
        self.exercicio_antigo = Exercicio.objects.create(
            nome="Supino",
            descricao="Exercício antigo",
            treino=self.treino
        )
        self.exercicio_novo = Exercicio.objects.create(
            nome="Supino Inclinado",
            descricao="Exercício novo",
            treino=self.treino
        )
    
    def test_troca_exercicio_creation(self):
        troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Preferência pessoal"
        )
        self.assertEqual(troca.cliente, self.cliente)
        self.assertEqual(troca.exercicio_antigo, self.exercicio_antigo)
        self.assertEqual(troca.exercicio_novo, self.exercicio_novo)
        self.assertEqual(troca.motivo, "Preferência pessoal")
    
    def test_troca_exercicio_str_representation(self):
        troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Preferência pessoal"
        )
        expected = f"{self.cliente.nome} - {self.exercicio_antigo.nome} → {self.exercicio_novo.nome}"
        self.assertEqual(str(troca), expected)
    
    def test_troca_exercicio_status_default(self):
        troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Teste"
        )
        # Verificar se o status padrão é PENDENTE
        self.assertEqual(troca.status, TrocaExercicio.PENDENTE)
    
    def test_troca_exercicio_status_choices(self):
        troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Teste",
            status=TrocaExercicio.APROVADA
        )
        self.assertEqual(troca.status, TrocaExercicio.APROVADA)
        
        troca.status = TrocaExercicio.REJEITADA
        troca.save()
        self.assertEqual(troca.status, TrocaExercicio.REJEITADA)
    
    def test_troca_exercicio_data_troca_auto(self):
        troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Teste"
        )
        # Verificar se data_troca foi definida automaticamente
        self.assertIsNotNone(troca.data_troca)
    
    def test_multiple_trocas_per_cliente(self):
        troca1 = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Troca 1"
        )
        
        exercicio_outro = Exercicio.objects.create(
            nome="Leg Press",
            treino=self.treino
        )
        
        troca2 = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_novo,
            exercicio_novo=exercicio_outro,
            motivo="Troca 2"
        )
        
        trocas_do_cliente = TrocaExercicio.objects.filter(cliente=self.cliente)
        self.assertEqual(trocas_do_cliente.count(), 2)