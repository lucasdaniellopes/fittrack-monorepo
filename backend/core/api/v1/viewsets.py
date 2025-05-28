from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser as DRFIsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao
from .serializers import (TreinoSerializer, DietaSerializer, TipoPlanoSerializer,
                        ClienteSerializer, HistoricoTreinoSerializer, HistoricoDietaSerializer,
                        ExercicioSerializer, RefeicaoSerializer, TrocaExercicioSerializer,
                        TrocaRefeicaoSerializer, UserSerializer, PerfilSerializer)
from .permissions import (IsAdminUser, IsNutricionistaUser, IsPersonalUser, 
                        IsClienteUser, IsOwnerOrStaff, ReadOnly)

class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(tags=['Default'])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TreinoViewSet(SoftDeleteModelViewSet):
    queryset = Treino.objects.filter(deleted_at__isnull=True)
    serializer_class = TreinoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsPersonalUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                # Clientes só podem ver seus próprios treinos
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return Treino.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        # Se o cliente não tem objeto Cliente associado, não mostra nenhum treino
                        return Treino.objects.none()
                except:
                    return Treino.objects.none()
            elif user.perfil.tipo in ['admin', 'personal']:
                return Treino.objects.filter(deleted_at__isnull=True)
        if user.is_superuser:
            return Treino.objects.filter(deleted_at__isnull=True)
        return Treino.objects.none()
    
    @swagger_auto_schema(tags=['Treinos'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Se a criação do treino foi bem-sucedida, criar um registro no histórico
        if response.status_code == 201:
            treino_id = response.data.get('id')
            cliente_id = response.data.get('cliente')
            
            if treino_id and cliente_id:
                treino = Treino.objects.get(id=treino_id)
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Criar registro no histórico
                HistoricoTreino.objects.create(
                    cliente=cliente,
                    treino=treino,
                    data_inicio=timezone.now().date()
                )
                
                # Atualizar a data do último treino do cliente
                cliente.data_ultimo_treino = timezone.now().date()
                cliente.save(update_fields=['data_ultimo_treino'])
        
        return response
    
    @swagger_auto_schema(tags=['Treinos'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DietaViewSet(SoftDeleteModelViewSet):
    queryset = Dieta.objects.filter(deleted_at__isnull=True)
    serializer_class = DietaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsNutricionistaUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                # Clientes só podem ver suas próprias dietas
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return Dieta.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        # Se o cliente não tem objeto Cliente associado, não mostra nenhuma dieta
                        return Dieta.objects.none()
                except:
                    return Dieta.objects.none()
            elif user.perfil.tipo in ['admin', 'nutricionista']:
                return Dieta.objects.filter(deleted_at__isnull=True)
        if user.is_superuser:
            return Dieta.objects.filter(deleted_at__isnull=True)
        return Dieta.objects.none()
    
    @swagger_auto_schema(tags=['Dietas'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            dieta_id = response.data.get('id')
            cliente_id = response.data.get('cliente')
            
            if dieta_id and cliente_id:
                dieta = Dieta.objects.get(id=dieta_id)
                cliente = Cliente.objects.get(id=cliente_id)
                
                HistoricoDieta.objects.create(
                    cliente=cliente,
                    dieta=dieta,
                    data_inicio=timezone.now().date()
                )
                
                
                cliente.data_ultima_dieta = timezone.now().date()
                cliente.save(update_fields=['data_ultima_dieta'])
        
        return response
    
    @swagger_auto_schema(tags=['Dietas'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TipoPlanoViewSet(SoftDeleteModelViewSet):
    queryset = TipoPlano.objects.filter(deleted_at__isnull=True)
    serializer_class = TipoPlanoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(tags=['Planos'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Planos'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Planos'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Planos'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Planos'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Planos'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ClienteViewSet(SoftDeleteModelViewSet):
    queryset = Cliente.objects.filter(deleted_at__isnull=True)
    serializer_class = ClienteSerializer
    
    def get_permissions(self):
        if self.action in ['list']:
            # Permite que usuários staff ou com perfil adequado listem clientes
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        # Se é superuser ou staff, pode ver todos os clientes
        if user.is_superuser or user.is_staff:
            return Cliente.objects.filter(deleted_at__isnull=True)
            
        # Se tem perfil, aplica as regras baseadas no tipo
        if hasattr(user, 'perfil') and user.perfil:
            if user.perfil.tipo == 'cliente' and hasattr(user.perfil, 'cliente'):
                return Cliente.objects.filter(deleted_at__isnull=True, perfil__usuario=user)
            elif user.perfil.tipo in ['admin', 'nutricionista', 'personal']:
                return Cliente.objects.filter(deleted_at__isnull=True)
                
        return Cliente.objects.none()
    
    @swagger_auto_schema(tags=['Clientes'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Clientes'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Clientes'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Clientes'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Clientes'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Clientes'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class HistoricoTreinoViewSet(SoftDeleteModelViewSet):
    queryset = HistoricoTreino.objects.filter(deleted_at__isnull=True)
    serializer_class = HistoricoTreinoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsPersonalUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return HistoricoTreino.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        return HistoricoTreino.objects.filter(deleted_at__isnull=True)
                except:
                    return HistoricoTreino.objects.filter(deleted_at__isnull=True)
            elif user.perfil.tipo in ['admin', 'personal']:
                return HistoricoTreino.objects.filter(deleted_at__isnull=True)
        return HistoricoTreino.objects.filter(deleted_at__isnull=True)
    
    @swagger_auto_schema(tags=['Histórico'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class HistoricoDietaViewSet(SoftDeleteModelViewSet):
    queryset = HistoricoDieta.objects.filter(deleted_at__isnull=True)
    serializer_class = HistoricoDietaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsNutricionistaUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return HistoricoDieta.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        return HistoricoDieta.objects.filter(deleted_at__isnull=True)
                except:
                    return HistoricoDieta.objects.filter(deleted_at__isnull=True)
            elif user.perfil.tipo in ['admin', 'nutricionista']:
                return HistoricoDieta.objects.filter(deleted_at__isnull=True)
        return HistoricoDieta.objects.filter(deleted_at__isnull=True)
    
    @swagger_auto_schema(tags=['Histórico'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ExercicioViewSet(SoftDeleteModelViewSet):
    queryset = Exercicio.objects.filter(deleted_at__isnull=True)
    serializer_class = ExercicioSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsPersonalUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente' and hasattr(user.perfil, 'cliente'):
                # Cliente vê apenas exercícios de seus treinos
                return Exercicio.objects.filter(deleted_at__isnull=True, treino__cliente__perfil__usuario=user)
            elif user.perfil.tipo in ['admin', 'personal']:
                # Admin e personal veem todos os exercícios
                return Exercicio.objects.filter(deleted_at__isnull=True)
        if user.is_superuser:
            return Exercicio.objects.filter(deleted_at__isnull=True)
        return Exercicio.objects.none()
    
    @swagger_auto_schema(tags=['Treinos'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Treinos'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RefeicaoViewSet(SoftDeleteModelViewSet):
    queryset = Refeicao.objects.filter(deleted_at__isnull=True)
    serializer_class = RefeicaoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, (IsAdminUser | IsNutricionistaUser)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente' and hasattr(user.perfil, 'cliente'):
                # Cliente vê apenas refeições de suas dietas
                return Refeicao.objects.filter(deleted_at__isnull=True, dieta__cliente__perfil__usuario=user)
            elif user.perfil.tipo in ['admin', 'nutricionista']:
                # Admin e nutricionista veem todas as refeições
                return Refeicao.objects.filter(deleted_at__isnull=True)
        if user.is_superuser:
            return Refeicao.objects.filter(deleted_at__isnull=True)
        return Refeicao.objects.none()
    
    @swagger_auto_schema(tags=['Dietas'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Dietas'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TrocaExercicioViewSet(SoftDeleteModelViewSet):
    queryset = TrocaExercicio.objects.filter(deleted_at__isnull=True)
    serializer_class = TrocaExercicioSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, IsClienteUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return TrocaExercicio.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        return TrocaExercicio.objects.filter(deleted_at__isnull=True)
                except:
                    return TrocaExercicio.objects.filter(deleted_at__isnull=True)
            elif user.perfil.tipo in ['admin', 'personal']:
                return TrocaExercicio.objects.filter(deleted_at__isnull=True)
        return TrocaExercicio.objects.filter(deleted_at__isnull=True)
    
    @swagger_auto_schema(tags=['Trocas'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsPersonalUser)])
    @swagger_auto_schema(tags=['Trocas'])
    def aprovar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'APROVADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        # Se há observações na request, salvar
        if 'observacoes_resposta' in request.data:
            troca.observacoes_resposta = request.data['observacoes_resposta']
        
        troca.save()
        
        return Response({'message': 'Solicitação aprovada com sucesso'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsPersonalUser)])
    @swagger_auto_schema(tags=['Trocas'])
    def rejeitar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'REJEITADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        # Observações são obrigatórias para rejeição
        if 'observacoes_resposta' not in request.data or not request.data['observacoes_resposta']:
            return Response({'error': 'Observações são obrigatórias para rejeitar uma solicitação'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.observacoes_resposta = request.data['observacoes_resposta']
        troca.save()
        
        return Response({'message': 'Solicitação rejeitada'}, status=status.HTTP_200_OK)


class TrocaRefeicaoViewSet(SoftDeleteModelViewSet):
    queryset = TrocaRefeicao.objects.filter(deleted_at__isnull=True)
    serializer_class = TrocaRefeicaoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, IsClienteUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.tipo == 'cliente':
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return TrocaRefeicao.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
                        return TrocaRefeicao.objects.filter(deleted_at__isnull=True)
                except:
                    return TrocaRefeicao.objects.filter(deleted_at__isnull=True)
            elif user.perfil.tipo in ['admin', 'nutricionista']:
                return TrocaRefeicao.objects.filter(deleted_at__isnull=True)
        return TrocaRefeicao.objects.filter(deleted_at__isnull=True)
    
    @swagger_auto_schema(tags=['Trocas'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsNutricionistaUser)])
    @swagger_auto_schema(tags=['Trocas'])
    def aprovar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'APROVADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        # Se há observações na request, salvar
        if 'observacoes_resposta' in request.data:
            troca.observacoes_resposta = request.data['observacoes_resposta']
        
        troca.save()
        
        return Response({'message': 'Solicitação aprovada com sucesso'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsNutricionistaUser)])
    @swagger_auto_schema(tags=['Trocas'])
    def rejeitar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'REJEITADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        # Observações são obrigatórias para rejeição
        if 'observacoes_resposta' not in request.data or not request.data['observacoes_resposta']:
            return Response({'error': 'Observações são obrigatórias para rejeitar uma solicitação'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.observacoes_resposta = request.data['observacoes_resposta']
        troca.save()
        
        return Response({'message': 'Solicitação rejeitada'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'me']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or (hasattr(user, 'perfil') and user.perfil.tipo == 'admin'):
            return User.objects.filter(is_active=True).order_by('-date_joined')
        return User.objects.filter(id=user.id, is_active=True).order_by('-date_joined')
    
    @swagger_auto_schema(tags=['Usuários'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def create(self, request, *args, **kwargs):
        # Debug para ver o que está sendo enviado
        print("Create User Request Data:", request.data)
        
        try:
            # O serializer agora cuida do tipo_perfil
            response = super().create(request, *args, **kwargs)
            return response
        except Exception as e:
            print("Error creating user:", str(e))
            raise
    
    @swagger_auto_schema(tags=['Usuários'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=['Usuários'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PerfilViewSet(SoftDeleteModelViewSet):
    queryset = Perfil.objects.filter(deleted_at__isnull=True)
    serializer_class = PerfilSerializer
    
    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAuthenticated]  # Permite clientes listarem perfis (filtrado no get_queryset)
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or (hasattr(user, 'perfil') and user.perfil.tipo == 'admin'):
            return Perfil.objects.filter(deleted_at__isnull=True)
        return Perfil.objects.filter(usuario=user, deleted_at__isnull=True)
    
    @swagger_auto_schema(tags=['Usuários'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def create(self, request, *args, **kwargs):
        # If usuario is not provided, use the current authenticated user
        if 'usuario' not in request.data:
            request.data['usuario'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Usuários'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
