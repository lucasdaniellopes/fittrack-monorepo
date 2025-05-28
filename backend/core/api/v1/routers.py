from rest_framework.routers import DefaultRouter
from .viewsets import (
    TreinoViewSet, DietaViewSet, TipoPlanoViewSet, ClienteViewSet, 
    HistoricoTreinoViewSet, HistoricoDietaViewSet, ExercicioViewSet, 
    RefeicaoViewSet, TrocaExercicioViewSet, TrocaRefeicaoViewSet,
    UserViewSet, PerfilViewSet
)

router = DefaultRouter()


router.register(r'treinos', TreinoViewSet)
router.register(r'dietas', DietaViewSet)
router.register(r'tipos-plano', TipoPlanoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'historico-treinos', HistoricoTreinoViewSet)
router.register(r'historico-dietas', HistoricoDietaViewSet)
router.register(r'exercicios', ExercicioViewSet)
router.register(r'refeicoes', RefeicaoViewSet)
router.register(r'trocas-exercicios', TrocaExercicioViewSet)
router.register(r'trocas-refeicoes', TrocaRefeicaoViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'perfis', PerfilViewSet)
