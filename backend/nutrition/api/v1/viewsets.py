from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from accounts.models import Cliente
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao
from .serializers import DietaSerializer, RefeicaoSerializer, HistoricoDietaSerializer, TrocaRefeicaoSerializer
from core.api.v1.permissions import (IsAdminUser, IsNutricionistaUser, IsClienteUser, IsOwnerOrStaff)
from core.api.v1.viewsets import SoftDeleteModelViewSet

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
                try:
                    if hasattr(user.perfil, 'cliente') and user.perfil.cliente:
                        return Dieta.objects.filter(deleted_at__isnull=True, cliente=user.perfil.cliente)
                    else:
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
                return Refeicao.objects.filter(deleted_at__isnull=True, dieta__cliente__perfil__usuario=user)
            elif user.perfil.tipo in ['admin', 'nutricionista']:
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
        
        if 'observacoes_resposta' not in request.data or not request.data['observacoes_resposta']:
            return Response({'error': 'Observações são obrigatórias para rejeitar uma solicitação'}, status=status.HTTP_400_BAD_REQUEST)
        
        troca.observacoes_resposta = request.data['observacoes_resposta']
        troca.save()
        
        return Response({'message': 'Solicitação rejeitada'}, status=status.HTTP_200_OK)