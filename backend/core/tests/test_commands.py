from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente
from workouts.models import Treino, Exercicio, TrocaExercicio
from core.commands.exchange_commands import (
    ApproveExerciseExchangeCommand,
    RejectExerciseExchangeCommand,
    ExchangeCommandFactory
)


class ExchangeCommandTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
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
        
        self.troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Preferência pessoal",
            status=TrocaExercicio.PENDENTE
        )
    
    def test_approve_exercise_exchange_command(self):
        command = ApproveExerciseExchangeCommand(self.troca.id)
        result = command.execute()
        
        self.assertTrue(result['success'])
        self.troca.refresh_from_db()
        self.assertEqual(self.troca.status, TrocaExercicio.APROVADA)
    
    def test_reject_exercise_exchange_command(self):
        command = RejectExerciseExchangeCommand(self.troca.id, "Motivo da rejeição")
        result = command.execute()
        
        self.assertTrue(result['success'])
        self.troca.refresh_from_db()
        self.assertEqual(self.troca.status, TrocaExercicio.REJEITADA)
    
    def test_command_factory_approve(self):
        command = ExchangeCommandFactory.create_command(
            'approve_exercise', 
            self.troca.id
        )
        self.assertIsInstance(command, ApproveExerciseExchangeCommand)
    
    def test_command_factory_reject(self):
        command = ExchangeCommandFactory.create_command(
            'reject_exercise', 
            self.troca.id, 
            rejection_reason="Motivo teste"
        )
        self.assertIsInstance(command, RejectExerciseExchangeCommand)
    
    def test_command_factory_invalid_type(self):
        with self.assertRaises(ValueError):
            ExchangeCommandFactory.create_command('invalid_type', self.troca.id)
    
    def test_command_undo_functionality(self):
        # Testar funcionalidade de undo se implementada
        command = ApproveExerciseExchangeCommand(self.troca.id)
        original_status = self.troca.status
        
        # Executar comando
        command.execute()
        self.troca.refresh_from_db()
        self.assertEqual(self.troca.status, TrocaExercicio.APROVADA)
        
        # Undo (se implementado)
        if hasattr(command, 'undo'):
            command.undo()
            self.troca.refresh_from_db()
            self.assertEqual(self.troca.status, original_status)