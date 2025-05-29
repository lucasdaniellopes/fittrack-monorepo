from rest_framework.routers import DefaultRouter
from .viewsets import (UserViewSet, PerfilViewSet, TipoPlanoViewSet, 
                       ClienteViewSet, PersonalViewSet, NutricionistaViewSet)

router = DefaultRouter()

router.register(r'usuarios', UserViewSet)
router.register(r'perfis', PerfilViewSet)
router.register(r'tipos-plano', TipoPlanoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'personais', PersonalViewSet)
router.register(r'nutricionistas', NutricionistaViewSet)

urlpatterns = router.urls