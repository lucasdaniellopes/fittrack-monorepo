from rest_framework.routers import DefaultRouter
from .viewsets import DietaViewSet, RefeicaoViewSet, HistoricoDietaViewSet, TrocaRefeicaoViewSet

router = DefaultRouter()

router.register(r'dietas', DietaViewSet)
router.register(r'refeicoes', RefeicaoViewSet)
router.register(r'historico-dietas', HistoricoDietaViewSet)
router.register(r'trocas-refeicoes', TrocaRefeicaoViewSet)

urlpatterns = router.urls