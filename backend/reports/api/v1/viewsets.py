from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from core.api.v1.permissions import IsAdminUser

class BaseReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags=['Relatórios'])
    def list(self, request):
        return Response({'message': 'Reports endpoint placeholder'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    @swagger_auto_schema(tags=['Relatórios'])
    def dashboard(self, request):
        return Response({'message': 'Dashboard data placeholder'})