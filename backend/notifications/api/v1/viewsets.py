from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

class BaseNotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags=['Notificações'])
    def list(self, request):
        return Response({'message': 'Notifications endpoint placeholder'})
    
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(tags=['Notificações'])
    def mark_all_read(self, request):
        return Response({'message': 'All notifications marked as read'})