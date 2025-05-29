from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente, Personal, Nutricionista
from .serializers import (UserSerializer, PerfilSerializer, TipoPlanoSerializer, 
                         ClienteSerializer, PersonalSerializer, NutricionistaSerializer)
from core.api.v1.permissions import (IsAdminUser, IsOwnerOrStaff)
from core.api.v1.viewsets import SoftDeleteModelViewSet

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'me']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == 'register':
            permission_classes = [AllowAny]
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
        print("Create User Request Data:", request.data)
        
        try:
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
    
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=['Usuários'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerfilViewSet(SoftDeleteModelViewSet):
    queryset = Perfil.objects.filter(deleted_at__isnull=True)
    serializer_class = PerfilSerializer
    
    def get_permissions(self):
        if self.action in ['list']:
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
        
        if user.is_superuser or user.is_staff:
            return Cliente.objects.filter(deleted_at__isnull=True)
            
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

class PersonalViewSet(SoftDeleteModelViewSet):
    queryset = Personal.objects.filter(deleted_at__isnull=True)
    serializer_class = PersonalSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or (hasattr(user, 'perfil') and user.perfil.tipo in ['admin', 'personal']):
            return Personal.objects.filter(deleted_at__isnull=True)
        return Personal.objects.none()
    
    @swagger_auto_schema(tags=['Personais'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Personais'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Personais'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Personais'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Personais'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Personais'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class NutricionistaViewSet(SoftDeleteModelViewSet):
    queryset = Nutricionista.objects.filter(deleted_at__isnull=True)
    serializer_class = NutricionistaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or (hasattr(user, 'perfil') and user.perfil.tipo in ['admin', 'nutricionista']):
            return Nutricionista.objects.filter(deleted_at__isnull=True)
        return Nutricionista.objects.none()
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['Nutricionistas'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)