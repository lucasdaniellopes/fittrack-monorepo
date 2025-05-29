from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from accounts.models import Cliente
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio
from .serializers import TreinoSerializer, ExercicioSerializer, HistoricoTreinoSerializer, TrocaExercicioSerializer
from core.api.v1.permissions import (IsAdminUser, IsPersonalUser, IsClienteUser, IsOwnerOrStaff)
from core.api.v1.viewsets import SoftDeleteModelViewSet

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
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return Treino.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
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
        
        if response.status_code == 201:
            treino_id = response.data.get('id')
            cliente_id = response.data.get('cliente')
            
            if treino_id and cliente_id:
                treino = Treino.objects.get(id=treino_id)
                cliente = Cliente.objects.get(id=cliente_id)
                
                HistoricoTreino.objects.create(
                    cliente=cliente,
                    treino=treino,
                    data_inicio=timezone.now().date()
                )
                
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
                return Exercicio.objects.filter(deleted_at__isnull=True, treino__cliente__perfil__usuario=user)
            elif user.perfil.tipo in ['admin', 'personal']:
                return Exercicio.objects.filter(deleted_at__isnull=True)
        if user.is_superuser:
            return Exercicio.objects.filter(deleted_at__isnull=True)
        return Exercicio.objects.none()
    
    @swagger_auto_schema(tags=['Exercícios'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Exercícios'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Exercícios'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Exercícios'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Exercícios'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Exercícios'])
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
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Histórico Treinos'])
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
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsPersonalUser)])
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def aprovar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'APROVADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        if 'observacoes_resposta' in request.data:
            troca.observacoes_resposta = request.data['observacoes_resposta']
        
        troca.save()
        
        return Response({'message': 'Solicitação aprovada com sucesso'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, (IsAdminUser | IsPersonalUser)])
    @swagger_auto_schema(tags=['Trocas Exercícios'])
    def rejeitar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'PENDENTE':
            return Response({'error': 'Solicitação já foi processada'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.status = 'REJEITADO'
        troca.aprovado_por = request.user
        troca.data_resposta = timezone.now()
        
        if 'observacoes_resposta' not in request.data or not request.data['observacoes_resposta']:
            return Response({'error': 'Observações são obrigatórias para rejeitar uma solicitação'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.observacoes_resposta = request.data['observacoes_resposta']
        troca.save()
        
        return Response({'message': 'Solicitação rejeitada'}, status=status.HTTP_200_OK)