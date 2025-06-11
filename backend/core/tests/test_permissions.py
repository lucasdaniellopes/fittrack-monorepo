from rest_framework import status
from core.tests.test_base import BaseTestCase


class PermissionsTest(BaseTestCase):
    """Testes para sistema de permissões"""
    
    def test_admin_acesso_total(self):
        """Testa se admin tem acesso a endpoints administrativos"""
        self.authenticate_user(self.admin_user)
        
        # Lista de endpoints que só admin deveria acessar
        admin_endpoints = [
            '/api/v1/admin/',
            '/api/v1/users/',
        ]
        
        for endpoint in admin_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                
                if response.status_code == 404:
                    continue  # Endpoint não existe ainda
                
                # Admin não deve receber 403 (Forbidden)
                self.assertNotEqual(
                    response.status_code, 
                    status.HTTP_403_FORBIDDEN,
                    f"Admin foi negado acesso a {endpoint}"
                )
    
    def test_cliente_acesso_limitado(self):
        """Testa se cliente tem acesso limitado"""
        self.authenticate_user(self.cliente_user)
        
        # Endpoints que cliente NÃO deveria acessar
        forbidden_endpoints = [
            '/api/v1/admin/',
            '/api/v1/users/',
        ]
        
        for endpoint in forbidden_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                
                if response.status_code == 404:
                    continue  # Endpoint não existe ainda
                
                # Cliente deve receber 403 (Forbidden) ou 401 (Unauthorized)
                self.assertIn(
                    response.status_code,
                    [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED],
                    f"Cliente teve acesso permitido a {endpoint}"
                )
    
    def test_nutricionista_acesso_especifico(self):
        """Testa acessos específicos do nutricionista"""
        self.authenticate_user(self.nutricionista_user)
        
        # Endpoints que nutricionista deveria acessar
        allowed_endpoints = [
            '/api/v1/dietas/',
            '/api/v1/refeicoes/',
        ]
        
        for endpoint in allowed_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                
                if response.status_code == 404:
                    continue  # Endpoint não existe ainda
                
                # Nutricionista não deve ser negado
                self.assertNotEqual(
                    response.status_code,
                    status.HTTP_403_FORBIDDEN,
                    f"Nutricionista foi negado acesso a {endpoint}"
                )
    
    def test_personal_acesso_especifico(self):
        """Testa acessos específicos do personal trainer"""
        self.authenticate_user(self.personal_user)
        
        # Endpoints que personal deveria acessar
        allowed_endpoints = [
            '/api/v1/treinos/',
            '/api/v1/exercicios/',
        ]
        
        for endpoint in allowed_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                
                if response.status_code == 404:
                    continue  # Endpoint não existe ainda
                
                # Personal não deve ser negado
                self.assertNotEqual(
                    response.status_code,
                    status.HTTP_403_FORBIDDEN,
                    f"Personal foi negado acesso a {endpoint}"
                )
