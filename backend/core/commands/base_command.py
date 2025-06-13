from abc import ABC, abstractmethod
from typing import Any, Dict


class Command(ABC):
    """Base command interface"""
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the command and return result"""
        pass
    
    @abstractmethod
    def can_execute(self) -> bool:
        """Check if command can be executed"""
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        """Get error message if command cannot be executed"""
        pass


class CommandInvoker:
    """Invoker to execute commands"""
    
    def __init__(self):
        self._history = []
    
    def execute_command(self, command: Command) -> Dict[str, Any]:
        """Execute a command if it can be executed"""
        if not command.can_execute():
            return {
                'success': False,
                'error': command.get_error_message()
            }
        
        try:
            result = command.execute()
            self._history.append(command)
            return {
                'success': True,
                'data': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_history(self):
        """Get command execution history"""
        return self._history