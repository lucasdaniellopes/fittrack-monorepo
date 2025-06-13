from rest_framework import status
from rest_framework.response import Response
from core.commands.base_command import CommandInvoker
from core.commands.exchange_commands import ExchangeCommandFactory


class ExchangeCommandMixin:
    """Mixin to add command-based exchange processing to ViewSets"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_invoker = CommandInvoker()
    
    def process_exchange_approval(self, exchange_instance, exchange_type: str, observacoes: str = None):
        """Process exchange approval using command pattern"""
        command = ExchangeCommandFactory.create_approve_command(
            exchange_type, 
            exchange_instance, 
            self.request.user, 
            observacoes
        )
        
        result = self.command_invoker.execute_command(command)
        
        if result['success']:
            return Response(result['data'], status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': result['error']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def process_exchange_rejection(self, exchange_instance, exchange_type: str, observacoes: str):
        """Process exchange rejection using command pattern"""
        command = ExchangeCommandFactory.create_reject_command(
            exchange_type, 
            exchange_instance, 
            self.request.user, 
            observacoes
        )
        
        result = self.command_invoker.execute_command(command)
        
        if result['success']:
            return Response(result['data'], status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': result['error']}, 
                status=status.HTTP_400_BAD_REQUEST
            )