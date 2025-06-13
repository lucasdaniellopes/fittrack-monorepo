from django.utils import timezone
from django.contrib.auth.models import User
from .base_command import Command
from core.observers.observer_setup import event_bus
from typing import Any, Dict


class BaseExchangeCommand(Command):
    def __init__(self, exchange_instance, user: User, observacoes: str = None):
        self.exchange = exchange_instance
        self.user = user
        self.observacoes = observacoes
    
    def can_execute(self) -> bool:
        return self.exchange.status == 'PENDENTE'
    
    def get_error_message(self) -> str:
        if self.exchange.status != 'PENDENTE':
            return 'Solicitação já foi processada'
        return 'Não é possível processar esta solicitação'


class ApproveExerciseExchangeCommand(BaseExchangeCommand):
    def execute(self) -> Dict[str, Any]:
        self.exchange.status = 'APROVADO'
        self.exchange.aprovado_por = self.user
        self.exchange.data_resposta = timezone.now()
        
        if self.observacoes:
            self.exchange.observacoes_resposta = self.observacoes
        
        self.exchange.save()
        
        event_bus.notify('troca_aprovada', {
            'troca': self.exchange,
            'cliente': self.exchange.cliente,
            'tipo': 'exercicio',
            'aprovado_por': self.user
        })
        
        return {
            'message': 'Solicitação de troca de exercício aprovada com sucesso',
            'troca_id': self.exchange.id,
            'status': self.exchange.status
        }


class RejectExerciseExchangeCommand(BaseExchangeCommand):
    def can_execute(self) -> bool:
        base_check = super().can_execute()
        has_observacoes = bool(self.observacoes and self.observacoes.strip())
        return base_check and has_observacoes
    
    def get_error_message(self) -> str:
        if self.exchange.status != 'PENDENTE':
            return 'Solicitação já foi processada'
        if not self.observacoes or not self.observacoes.strip():
            return 'Observações são obrigatórias para rejeitar uma solicitação'
        return 'Não é possível rejeitar esta solicitação'
    
    def execute(self) -> Dict[str, Any]:
        self.exchange.status = 'REJEITADO'
        self.exchange.aprovado_por = self.user
        self.exchange.data_resposta = timezone.now()
        self.exchange.observacoes_resposta = self.observacoes
        
        self.exchange.save()
        
        event_bus.notify('troca_rejeitada', {
            'troca': self.exchange,
            'cliente': self.exchange.cliente,
            'tipo': 'exercicio',
            'rejeitado_por': self.user,
            'motivo': self.observacoes
        })
        
        return {
            'message': 'Solicitação de troca de exercício rejeitada',
            'troca_id': self.exchange.id,
            'status': self.exchange.status
        }


class ApproveMealExchangeCommand(BaseExchangeCommand):
    def execute(self) -> Dict[str, Any]:
        self.exchange.status = 'APROVADO'
        self.exchange.aprovado_por = self.user
        self.exchange.data_resposta = timezone.now()
        
        if self.observacoes:
            self.exchange.observacoes_resposta = self.observacoes
        
        self.exchange.save()
        
        event_bus.notify('troca_aprovada', {
            'troca': self.exchange,
            'cliente': self.exchange.cliente,
            'tipo': 'refeicao',
            'aprovado_por': self.user
        })
        
        return {
            'message': 'Solicitação de troca de refeição aprovada com sucesso',
            'troca_id': self.exchange.id,
            'status': self.exchange.status
        }


class RejectMealExchangeCommand(BaseExchangeCommand):
    def can_execute(self) -> bool:
        base_check = super().can_execute()
        has_observacoes = bool(self.observacoes and self.observacoes.strip())
        return base_check and has_observacoes
    
    def get_error_message(self) -> str:
        if self.exchange.status != 'PENDENTE':
            return 'Solicitação já foi processada'
        if not self.observacoes or not self.observacoes.strip():
            return 'Observações são obrigatórias para rejeitar uma solicitação'
        return 'Não é possível rejeitar esta solicitação'
    
    def execute(self) -> Dict[str, Any]:
        self.exchange.status = 'REJEITADO'
        self.exchange.aprovado_por = self.user
        self.exchange.data_resposta = timezone.now()
        self.exchange.observacoes_resposta = self.observacoes
        
        self.exchange.save()
        
        event_bus.notify('troca_rejeitada', {
            'troca': self.exchange,
            'cliente': self.exchange.cliente,
            'tipo': 'refeicao',
            'rejeitado_por': self.user,
            'motivo': self.observacoes
        })
        
        return {
            'message': 'Solicitação de troca de refeição rejeitada',
            'troca_id': self.exchange.id,
            'status': self.exchange.status
        }


class ExchangeCommandFactory:
    @staticmethod
    def create_approve_command(exchange_type: str, exchange_instance, user: User, observacoes: str = None):
        if exchange_type == 'exercicio':
            return ApproveExerciseExchangeCommand(exchange_instance, user, observacoes)
        elif exchange_type == 'refeicao':
            return ApproveMealExchangeCommand(exchange_instance, user, observacoes)
        else:
            raise ValueError(f"Unknown exchange type: {exchange_type}")
    
    @staticmethod
    def create_reject_command(exchange_type: str, exchange_instance, user: User, observacoes: str):
        if exchange_type == 'exercicio':
            return RejectExerciseExchangeCommand(exchange_instance, user, observacoes)
        elif exchange_type == 'refeicao':
            return RejectMealExchangeCommand(exchange_instance, user, observacoes)
        else:
            raise ValueError(f"Unknown exchange type: {exchange_type}")