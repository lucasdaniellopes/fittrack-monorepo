from rest_framework.routers import DefaultRouter

from accounts.api.v1.viewsets import (
    UserViewSet, PerfilViewSet, TipoPlanoViewSet, ClienteViewSet,
    PersonalViewSet, NutricionistaViewSet
)
from nutrition.api.v1.viewsets import (
    DietaViewSet, RefeicaoViewSet, HistoricoDietaViewSet, TrocaRefeicaoViewSet
)
from workouts.api.v1.viewsets import (
    TreinoViewSet, ExercicioViewSet, HistoricoTreinoViewSet, TrocaExercicioViewSet
)
from reports.api.v1.viewsets import BaseReportViewSet
from notifications.api.v1.viewsets import BaseNotificationViewSet

router = DefaultRouter()

router.register(r'usuarios', UserViewSet)
router.register(r'perfis', PerfilViewSet)
router.register(r'tipos-plano', TipoPlanoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'personais', PersonalViewSet)
router.register(r'nutricionistas', NutricionistaViewSet)

router.register(r'treinos', TreinoViewSet)
router.register(r'exercicios', ExercicioViewSet)
router.register(r'historico-treinos', HistoricoTreinoViewSet)
router.register(r'trocas-exercicios', TrocaExercicioViewSet)

router.register(r'dietas', DietaViewSet)
router.register(r'refeicoes', RefeicaoViewSet)
router.register(r'historico-dietas', HistoricoDietaViewSet)
router.register(r'trocas-refeicoes', TrocaRefeicaoViewSet)

router.register(r'reports', BaseReportViewSet, basename='reports')
router.register(r'notifications', BaseNotificationViewSet, basename='notifications')

urlpatterns = router.urls
