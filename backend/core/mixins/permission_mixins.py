from core.strategies.permission_strategies import PermissionStrategyFactory


class PermissionStrategyMixin:
    """Mixin to use permission strategies in ViewSets"""
    
    def get_permissions(self):
        """Get permissions using strategy pattern"""
        user = self.request.user if hasattr(self, 'request') else None
        if not user:
            return super().get_permissions()
        
        strategy = PermissionStrategyFactory.get_strategy(user)
        permission_classes = strategy.get_permissions_for_action(self.action)
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Get queryset using strategy pattern"""
        user = self.request.user if hasattr(self, 'request') else None
        if not user:
            return super().get_queryset()
        
        strategy = PermissionStrategyFactory.get_strategy(user)
        base_queryset = super().get_queryset()
        
        return strategy.filter_queryset(
            base_queryset, 
            user, 
            self.queryset.model if hasattr(self, 'queryset') else None
        )