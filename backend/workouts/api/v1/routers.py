from rest_framework.routers import DefaultRouter
from .viewsets import TreinoViewSet, ExercicioViewSet, HistoricoTreinoViewSet, TrocaExercicioViewSet

router = DefaultRouter()

router.register(r'treinos', TreinoViewSet)
router.register(r'exercicios', ExercicioViewSet)
router.register(r'historico-treinos', HistoricoTreinoViewSet)
router.register(r'trocas-exercicios', TrocaExercicioViewSet)

urlpatterns = router.urls