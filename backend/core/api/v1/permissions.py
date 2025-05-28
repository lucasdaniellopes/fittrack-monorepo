from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'admin'

class IsNutricionistaUser(permissions.BasePermission):
  
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'nutricionista'

class IsPersonalUser(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'personal'

class IsClienteUser(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'cliente'

class IsOwnerOrStaff(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.tipo in ['admin', 'nutricionista', 'personal']):
            return True
            
        
        if hasattr(obj, 'cliente') and hasattr(obj.cliente, 'perfil'):
            return obj.cliente.perfil.usuario == request.user
        elif hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        elif hasattr(obj, 'perfil') and hasattr(obj.perfil, 'usuario'):
            return obj.perfil.usuario == request.user
        return False

class ReadOnly(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
