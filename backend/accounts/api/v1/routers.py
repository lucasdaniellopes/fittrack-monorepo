from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (UserViewSet, PerfilViewSet, TipoPlanoViewSet, 
                       ClienteViewSet, PersonalViewSet, NutricionistaViewSet)

# Main router for accounts endpoints
router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'perfis', PerfilViewSet)
router.register(r'tipos-plano', TipoPlanoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'personais', PersonalViewSet)
router.register(r'nutricionistas', NutricionistaViewSet)

# Auth router for /api/v1/auth/ endpoints
auth_router = DefaultRouter()
auth_router.register(r'', UserViewSet, basename='auth')

urlpatterns = [
    # Include auth router for register endpoint
    path('', include(auth_router.urls)),
    # Include main router for other endpoints
    path('', include(router.urls)),
]