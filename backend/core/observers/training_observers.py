from django.utils import timezone
from .base_observer import Observer
from typing import Dict, Any


class HistoryObserver(Observer):
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == 'treino_created':
            self._create_training_history(data)
        elif event_type == 'dieta_created':
            self._create_diet_history(data)
    
    def _create_training_history(self, data: Dict[str, Any]):
        try:
            from workouts.models import HistoricoTreino
            
            treino = data.get('treino')
            cliente = data.get('cliente')
            
            if treino and cliente:
                HistoricoTreino.objects.create(
                    cliente=cliente,
                    treino=treino,
                    data_inicio=timezone.now().date()
                )
                print(f"Histórico de treino criado para cliente {cliente.nome}")
        except Exception as e:
            print(f"Erro ao criar histórico de treino: {str(e)}")
    
    def _create_diet_history(self, data: Dict[str, Any]):
        try:
            from nutrition.models import HistoricoDieta
            
            dieta = data.get('dieta')
            cliente = data.get('cliente')
            
            if dieta and cliente:
                HistoricoDieta.objects.create(
                    cliente=cliente,
                    dieta=dieta,
                    data_inicio=timezone.now().date()
                )
                print(f"Histórico de dieta criado para cliente {cliente.nome}")
        except Exception as e:
            print(f"Erro ao criar histórico de dieta: {str(e)}")


class ClienteUpdateObserver(Observer):
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == 'treino_created':
            self._update_cliente_training_date(data)
        elif event_type == 'dieta_created':
            self._update_cliente_diet_date(data)
    
    def _update_cliente_training_date(self, data: Dict[str, Any]):
        try:
            cliente = data.get('cliente')
            if cliente:
                cliente.data_ultimo_treino = timezone.now().date()
                cliente.save(update_fields=['data_ultimo_treino'])
                print(f"Data último treino atualizada para cliente {cliente.nome}")
        except Exception as e:
            print(f"Erro ao atualizar data do treino: {str(e)}")
    
    def _update_cliente_diet_date(self, data: Dict[str, Any]):
        try:
            cliente = data.get('cliente')
            if cliente:
                cliente.data_ultima_dieta = timezone.now().date()
                cliente.save(update_fields=['data_ultima_dieta'])
                print(f"Data última dieta atualizada para cliente {cliente.nome}")
        except Exception as e:
            print(f"Erro ao atualizar data da dieta: {str(e)}")


class NotificationObserver(Observer):
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == 'treino_created':
            self._create_training_notification(data)
        elif event_type == 'dieta_created':
            self._create_diet_notification(data)
        elif event_type == 'troca_aprovada':
            self._create_exchange_approved_notification(data)
        elif event_type == 'troca_rejeitada':
            self._create_exchange_rejected_notification(data)
    
    def _create_training_notification(self, data: Dict[str, Any]):
        print(f"Notificação: Novo treino criado para cliente {data.get('cliente', {}).nome if data.get('cliente') else 'desconhecido'}")
    
    def _create_diet_notification(self, data: Dict[str, Any]):
        print(f"Notificação: Nova dieta criada para cliente {data.get('cliente', {}).nome if data.get('cliente') else 'desconhecido'}")
    
    def _create_exchange_approved_notification(self, data: Dict[str, Any]):
        cliente = data.get('cliente')
        if cliente:
            print(f"Notificação: Solicitação de troca aprovada para cliente {cliente.nome}")
    
    def _create_exchange_rejected_notification(self, data: Dict[str, Any]):
        cliente = data.get('cliente')
        if cliente:
            print(f"Notificação: Solicitação de troca rejeitada para cliente {cliente.nome}")