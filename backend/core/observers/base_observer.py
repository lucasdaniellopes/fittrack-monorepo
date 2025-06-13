from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Observer(ABC):
    """Base observer interface"""
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]):
        """Handle an event notification"""
        pass


class Subject:
    """Subject that notifies observers of events"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Dict[str, Any]):
        """Notify all observers of an event"""
        for observer in self._observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                print(f"Error notifying observer {observer.__class__.__name__}: {str(e)}")


class EventBus(Subject):
    """Global event bus for the application"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True