"""
Utility functions and base classes for testing.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Perfil, Cliente, TipoPlano


class BaseTestCase(TestCase):
    """Base test case with common setup for all tests."""
    
    def setUp(self):
        """Set up common test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        
        self.tipo_plano = TipoPlano.objects.create(
            nome="Plano Teste",
            descricao="Plano para testes",
            preco="99.90",
            duracao_dias=30,
            limite_trocas_exercicios=5,
            limite_trocas_refeicoes=3
        )
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil,
            tipo_plano=self.tipo_plano
        )


class BaseAPITestCase(APITestCase):
    """Base API test case with authentication setup."""
    
    def setUp(self):
        """Set up common test data for API tests."""
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        # Create regular client user
        self.client_user = User.objects.create_user(
            username='client',
            email='client@test.com',
            password='testpass123'
        )
        
        # Get or create profiles
        self.admin_perfil = Perfil.objects.get(usuario=self.admin_user)
        self.client_perfil = Perfil.objects.get(usuario=self.client_user)
        
        # Set correct profile types
        self.admin_perfil.tipo = Perfil.ADMIN
        self.admin_perfil.save()
        
        # Create tipo plano
        self.tipo_plano = TipoPlano.objects.create(
            nome="Plano API Teste",
            descricao="Plano para testes de API",
            preco="99.90",
            duracao_dias=30,
            limite_trocas_exercicios=5,
            limite_trocas_refeicoes=3
        )
        
        # Create cliente
        self.cliente = Cliente.objects.create(
            nome="Cliente API Teste",
            email="cliente_api@test.com",
            perfil=self.client_perfil,
            tipo_plano=self.tipo_plano
        )
        
        # Generate JWT tokens
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.client_token = str(RefreshToken.for_user(self.client_user).access_token)
    
    def authenticate_as_admin(self):
        """Authenticate request as admin user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
    
    def authenticate_as_client(self):
        """Authenticate request as client user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
    
    def clear_authentication(self):
        """Clear authentication credentials."""
        self.client.credentials()


class TestDataFactory:
    """Factory class to create test data objects."""
    
    @staticmethod
    def create_user(username='testuser', email='test@example.com', is_staff=False):
        """Create a test user."""
        return User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            is_staff=is_staff
        )
    
    @staticmethod
    def create_tipo_plano(nome='Plano Teste', preco='99.90'):
        """Create a test tipo plano."""
        return TipoPlano.objects.create(
            nome=nome,
            descricao=f"Descrição do {nome}",
            preco=preco,
            duracao_dias=30,
            limite_trocas_exercicios=5,
            limite_trocas_refeicoes=3
        )
    
    @staticmethod
    def create_cliente(nome='Cliente Teste', user=None, tipo_plano=None):
        """Create a test cliente."""
        if not user:
            user = TestDataFactory.create_user()
        
        perfil = Perfil.objects.get(usuario=user)
        
        return Cliente.objects.create(
            nome=nome,
            email=f"{nome.lower().replace(' ', '_')}@test.com",
            perfil=perfil,
            tipo_plano=tipo_plano
        )


def assert_api_response_structure(test_case, response_data, expected_fields):
    """
    Assert that API response contains expected fields.
    
    Args:
        test_case: TestCase instance
        response_data: Response data dict
        expected_fields: Set of expected field names
    """
    for field in expected_fields:
        test_case.assertIn(field, response_data, f"Campo {field} não encontrado na resposta")


def assert_pagination_structure(test_case, response_data):
    """
    Assert that API response has pagination structure.
    
    Args:
        test_case: TestCase instance
        response_data: Response data dict
    """
    expected_pagination_fields = {'count', 'next', 'previous', 'results'}
    for field in expected_pagination_fields:
        test_case.assertIn(field, response_data, f"Campo de paginação {field} não encontrado")


def create_test_image():
    """Create a test image for file upload tests."""
    from PIL import Image
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile
    
    # Create a small test image
    image = Image.new('RGB', (100, 100), color='red')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    
    return InMemoryUploadedFile(
        image_io,
        None,
        'test_image.jpg',
        'image/jpeg',
        image_io.getbuffer().nbytes,
        None
    )


class MockRequestUser:
    """Mock user for testing permissions and viewsets."""
    
    def __init__(self, user_type='cliente', is_staff=False, is_superuser=False):
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.user_type = user_type
        
        # Create actual user and perfil
        self.user = TestDataFactory.create_user(
            username=f'mock_{user_type}',
            is_staff=is_staff
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        
        # Set perfil type based on user_type
        if user_type == 'admin':
            self.perfil.tipo = Perfil.ADMIN
        elif user_type == 'nutricionista':
            self.perfil.tipo = Perfil.NUTRICIONISTA
        elif user_type == 'personal':
            self.perfil.tipo = Perfil.PERSONAL
        else:
            self.perfil.tipo = Perfil.CLIENTE
        
        self.perfil.save()
    
    def has_perm(self, perm):
        """Mock permission check."""
        if self.is_superuser:
            return True
        if self.is_staff and 'admin' in perm:
            return True
        return False


# Test decorators
def skip_if_no_db(test_func):
    """Decorator to skip test if database is not available."""
    import functools
    from django.test import override_settings
    
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        try:
            return test_func(*args, **kwargs)
        except Exception as e:
            if 'database' in str(e).lower():
                import unittest
                raise unittest.SkipTest(f"Database not available: {e}")
            raise
    return wrapper


def with_test_data(func):
    """Decorator to automatically create test data for a test method."""
    import functools
    
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Create additional test data if needed
        if not hasattr(self, 'extra_user'):
            self.extra_user = TestDataFactory.create_user('extrauser')
        
        if not hasattr(self, 'extra_tipo_plano'):
            self.extra_tipo_plano = TestDataFactory.create_tipo_plano('Plano Extra')
        
        return func(self, *args, **kwargs)
    
    return wrapper