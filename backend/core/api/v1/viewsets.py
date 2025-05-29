from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(tags=['Default'])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CoreAPIViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags=['Core'])
    def list(self, request):
        modules = {
            'message': 'FitTrack API v1',
            'modules': {
                'contas': '/api/v1/contas/',
                'nutricao': '/api/v1/nutricao/',
                'treinos': '/api/v1/treinos/',
                'relatorios': '/api/v1/relatorios/',
                'notificacoes': '/api/v1/notificacoes/'
            },
            'auth': {
                'login': '/api/v1/token/',
                'refresh': '/api/v1/token/refresh/',
                'register': '/api/v1/auth/register/'
            },
            'docs': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/'
            }
        }
        return Response(modules)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=['Core'])
    def status(self, request):
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now(),
            'user': request.user.username if request.user.is_authenticated else 'anonymous'
        })