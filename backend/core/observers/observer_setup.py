from .base_observer import EventBus
from .training_observers import HistoryObserver, ClienteUpdateObserver, NotificationObserver

# Global event bus instance
event_bus = EventBus()

def setup_observers():
    """Setup all observers in the event bus"""
    # Create observer instances
    history_observer = HistoryObserver()
    cliente_update_observer = ClienteUpdateObserver()
    notification_observer = NotificationObserver()
    
    # Attach observers to event bus
    event_bus.attach(history_observer)
    event_bus.attach(cliente_update_observer)
    event_bus.attach(notification_observer)
    
    print("Observers configurados no EventBus")
    
    return event_bus