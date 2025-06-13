from django.test import TestCase
from accounts.models import Perfil
from core.strategies.permission_strategies import PermissionStrategyFactory


class PermissionStrategyTest(TestCase):
    def test_admin_permission_strategy(self):
        # Teste direto da strategy sem criar usuários
        from core.strategies.permission_strategies import AdminPermissionStrategy
        strategy = AdminPermissionStrategy()
        permissions = strategy.get_permissions()
        self.assertGreater(len(permissions), 0)
        # Verificar se contém permissões de admin
        permission_names = [p.__name__ for p in permissions]
        self.assertIn('IsAuthenticated', permission_names)
    
    def test_cliente_permission_strategy(self):
        from core.strategies.permission_strategies import ClientePermissionStrategy
        strategy = ClientePermissionStrategy()
        permissions = strategy.get_permissions()
        self.assertGreater(len(permissions), 0)
        # Verificar se contém permissões de cliente
        permission_names = [p.__name__ for p in permissions]
        self.assertIn('IsAuthenticated', permission_names)
    
    def test_personal_permission_strategy(self):
        from core.strategies.permission_strategies import PersonalPermissionStrategy
        strategy = PersonalPermissionStrategy()
        permissions = strategy.get_permissions()
        self.assertGreater(len(permissions), 0)
    
    def test_nutricionista_permission_strategy(self):
        from core.strategies.permission_strategies import NutricionistaPermissionStrategy
        strategy = NutricionistaPermissionStrategy()
        permissions = strategy.get_permissions()
        self.assertGreater(len(permissions), 0)
    
    def test_strategy_types_are_different(self):
        from core.strategies.permission_strategies import (
            AdminPermissionStrategy, 
            ClientePermissionStrategy
        )
        admin_strategy = AdminPermissionStrategy()
        client_strategy = ClientePermissionStrategy()
        
        self.assertNotEqual(type(admin_strategy), type(client_strategy))