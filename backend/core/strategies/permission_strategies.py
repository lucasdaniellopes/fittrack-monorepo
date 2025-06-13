from abc import ABC, abstractmethod
from rest_framework.permissions import IsAuthenticated
from core.api.v1.permissions import IsAdminUser, IsOwnerOrStaff, IsNutricionistaUser, IsPersonalUser, IsClienteUser


class PermissionStrategy(ABC):
    """Base strategy for handling permissions and queryset filtering"""
    
    @abstractmethod
    def get_permissions_for_action(self, action):
        """Return permission classes for a given action"""
        pass
    
    @abstractmethod
    def filter_queryset(self, queryset, user, model_class=None):
        """Filter queryset based on user permissions"""
        pass


class AdminPermissionStrategy(PermissionStrategy):
    """Strategy for admin users - full access"""
    
    def get_permissions_for_action(self, action):
        if action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated, IsAdminUser]
        elif action == 'destroy':
            return [IsAuthenticated, IsAdminUser]
        return [IsAuthenticated]
    
    def filter_queryset(self, queryset, user, model_class=None):
        # Admin sees everything
        return queryset


class ClientePermissionStrategy(PermissionStrategy):
    """Strategy for client users - limited access"""
    
    def get_permissions_for_action(self, action):
        if action in ['list', 'retrieve']:
            return [IsAuthenticated, IsOwnerOrStaff]
        elif action in ['create']:
            return [IsAuthenticated, IsClienteUser]
        elif action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated, IsOwnerOrStaff]
        return [IsAuthenticated]
    
    def filter_queryset(self, queryset, user, model_class=None):
        # Cliente only sees their own data
        if hasattr(user, 'perfil') and hasattr(user.perfil, 'cliente'):
            return queryset.filter(cliente=user.perfil.cliente)
        return queryset.none()


class NutricionistaPermissionStrategy(PermissionStrategy):
    """Strategy for nutritionist users"""
    
    def get_permissions_for_action(self, action):
        if action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated, (IsAdminUser | IsNutricionistaUser)]
        elif action == 'destroy':
            return [IsAuthenticated, IsAdminUser]
        return [IsAuthenticated]
    
    def filter_queryset(self, queryset, user, model_class=None):
        # Nutricionista sees all nutrition-related data
        return queryset


class PersonalPermissionStrategy(PermissionStrategy):
    """Strategy for personal trainer users"""
    
    def get_permissions_for_action(self, action):
        if action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated, (IsAdminUser | IsPersonalUser)]
        elif action == 'destroy':
            return [IsAuthenticated, IsAdminUser]
        return [IsAuthenticated]
    
    def filter_queryset(self, queryset, user, model_class=None):
        # Personal trainer sees all workout-related data
        return queryset


class PermissionStrategyFactory:
    """Factory to get the appropriate permission strategy based on user type"""
    
    _strategies = {
        'admin': AdminPermissionStrategy(),
        'cliente': ClientePermissionStrategy(),
        'nutricionista': NutricionistaPermissionStrategy(),
        'personal': PersonalPermissionStrategy(),
    }
    
    @classmethod
    def get_strategy(cls, user):
        """Get permission strategy based on user type"""
        if user.is_superuser or user.is_staff:
            return cls._strategies['admin']
        
        if hasattr(user, 'perfil') and user.perfil:
            user_type = user.perfil.tipo
            return cls._strategies.get(user_type, cls._strategies['cliente'])
        
        return cls._strategies['cliente']