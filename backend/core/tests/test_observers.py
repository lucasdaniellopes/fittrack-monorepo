from django.test import TestCase
from core.observers.base_observer import EventBus, Observer


class EventBusTest(TestCase):
    def setUp(self):
        self.event_bus = EventBus()
    
    def test_event_bus_initialization(self):
        self.assertIsInstance(self.event_bus._observers, list)
    
    def test_event_bus_attach_observer(self):
        class TestObserver(Observer):
            def update(self, event_type, data):
                pass
        
        observer = TestObserver()
        self.event_bus.attach(observer)
        self.assertIn(observer, self.event_bus._observers)
    
    def test_event_bus_detach_observer(self):
        class TestObserver(Observer):
            def update(self, event_type, data):
                pass
        
        observer = TestObserver()
        self.event_bus.attach(observer)
        self.assertIn(observer, self.event_bus._observers)
        
        self.event_bus.detach(observer)
        self.assertNotIn(observer, self.event_bus._observers)
    
    def test_event_bus_notify(self):
        notifications = []
        
        class TestObserver(Observer):
            def update(self, event_type, data):
                notifications.append({'event_type': event_type, 'data': data})
        
        observer = TestObserver()
        self.event_bus.attach(observer)
        test_data = {'message': 'test notification'}
        self.event_bus.notify('test_event', test_data)
        
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['event_type'], 'test_event')
        self.assertEqual(notifications[0]['data'], test_data)
    
    def test_event_bus_singleton(self):
        # Testar se EventBus é singleton
        bus1 = EventBus()
        bus2 = EventBus()
        self.assertIs(bus1, bus2)
    
    def test_observer_error_handling(self):
        class FaultyObserver(Observer):
            def update(self, event_type, data):
                raise Exception("Test error")
        
        class WorkingObserver(Observer):
            def __init__(self):
                self.received = False
            
            def update(self, event_type, data):
                self.received = True
        
        faulty = FaultyObserver()
        working = WorkingObserver()
        
        self.event_bus.attach(faulty)
        self.event_bus.attach(working)
        
        # Notificar - deve capturar erro do FaultyObserver mas continuar
        self.event_bus.notify('test', {})
        
        # O observer que funciona deve ter recebido a notificação
        self.assertTrue(working.received)