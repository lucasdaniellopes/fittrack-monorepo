from core.observers.observer_setup import event_bus


class EventNotifierMixin:
    """Mixin to add event notification capabilities to ViewSets"""
    
    def notify_event(self, event_type: str, **kwargs):
        """Notify observers of an event"""
        event_bus.notify(event_type, kwargs)
    
    def perform_create(self, serializer):
        """Override to notify observers after creation"""
        instance = serializer.save()
        self._notify_creation_event(instance, serializer)
        return instance
    
    def _notify_creation_event(self, instance, serializer):
        """Notify appropriate creation event based on model type"""
        model_name = instance.__class__.__name__.lower()
        
        if model_name == 'treino':
            self.notify_event(
                'treino_created',
                treino=instance,
                cliente=instance.cliente
            )
        elif model_name == 'dieta':
            self.notify_event(
                'dieta_created',
                dieta=instance,
                cliente=instance.cliente
            )