from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import Perfil


class BaseTestCase(APITestCase):
    """Classe base para todos os testes da API"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.client = APIClient()
        
        # Criar usuários de teste
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.cliente_user = User.objects.create_user(
            username='cliente_test',
            email='cliente@test.com',
            password='testpass123'
        )
        
        self.nutricionista_user = User.objects.create_user(
            username='nutricionista_test',
            email='nutricionista@test.com',
            password='testpass123'
        )
        
        self.personal_user = User.objects.create_user(
            username='personal_test',
            email='personal@test.com',
            password='testpass123'
        )
        
        # Criar perfis específicos (além dos criados automaticamente)
        perfil_nutri, created = Perfil.objects.get_or_create(
            usuario=self.nutricionista_user,
            defaults={'tipo': 'nutricionista'}
        )
        if not created:
            perfil_nutri.tipo = 'nutricionista'
            perfil_nutri.save()
        
        perfil_personal, created = Perfil.objects.get_or_create(
            usuario=self.personal_user,
            defaults={'tipo': 'personal'}
        )
        if not created:
            perfil_personal.tipo = 'personal'
            perfil_personal.save()
    
    def get_jwt_token(self, user):
        """Gera token JWT para um usuário"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def authenticate_user(self, user):
        """Autentica um usuário no client de teste"""
        token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return token
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.client.credentials()  
