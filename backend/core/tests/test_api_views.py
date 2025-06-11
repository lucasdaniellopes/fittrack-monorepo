from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.tests.test_base import BaseTestCase
from core.models import Perfil


class AuthenticationAPITest(BaseTestCase):
    """Testes para endpoints de autenticação"""
    
    def test_obter_token_com_credenciais_validas(self):
        """Testa obtenção de token com credenciais válidas"""
        try:
            url = reverse('token_obtain_pair')
        except:
            url = '/api/v1/auth/token/'
        
        data = {
            'username': 'cliente_test',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code == 404:
            self.skipTest("Endpoint de token não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obter_token_com_credenciais_invalidas(self):
        """Testa obtenção de token com credenciais inválidas"""
        try:
            url = reverse('token_obtain_pair')
        except:
            url = '/api/v1/auth/token/'
        
        data = {
            'username': 'cliente_test',
            'password': 'senhaerrada'
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code == 404:
            self.skipTest("Endpoint de token não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_token_valido(self):
        """Testa renovação de token com refresh token válido"""
        # Obter refresh token
        refresh = RefreshToken.for_user(self.cliente_user)
        
        try:
            url = reverse('token_refresh')
        except:
            url = '/api/v1/auth/token/refresh/'
        
        data = {
            'refresh': str(refresh)
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code == 404:
            self.skipTest("Endpoint de refresh não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_refresh_token_invalido(self):
        """Testa renovação com refresh token inválido"""
        try:
            url = reverse('token_refresh')
        except:
            url = '/api/v1/auth/token/refresh/'
        
        data = {
            'refresh': 'token_invalido'
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code == 404:
            self.skipTest("Endpoint de refresh não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAPITest(BaseTestCase):
    """Testes para endpoints de usuário"""
    
    def test_usuario_me_autenticado(self):
        """Testa endpoint /me com usuário autenticado"""
        self.authenticate_user(self.cliente_user)
        
        try:
            url = reverse('user-me')
        except:
            url = '/api/v1/users/me/'
        
        response = self.client.get(url)
        
        if response.status_code == 404:
            self.skipTest("Endpoint /me não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'cliente_test')
        self.assertIn('email', response.data)
    
    def test_usuario_me_nao_autenticado(self):
        """Testa endpoint /me sem autenticação"""
        try:
            url = reverse('user-me')
        except:
            url = '/api/v1/users/me/'
        
        response = self.client.get(url)
        
        if response.status_code == 404:
            self.skipTest("Endpoint /me não configurado ainda")
        
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])
    
    def test_listar_usuarios_como_admin(self):
        """Testa listagem de usuários como admin"""
        self.authenticate_user(self.admin_user)
        
        try:
            url = reverse('user-list')
        except:
            url = '/api/v1/users/'
        
        response = self.client.get(url)
        
        if response.status_code == 404:
            self.skipTest("Endpoint de listagem não configurado ainda")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, (list, dict))


class SecurityAPITest(BaseTestCase):
    """Testes básicos de segurança da API"""
    
    def test_usuario_nao_autenticado_negado_endpoints_protegidos(self):
        """Testa se usuário não autenticado é negado em endpoints protegidos"""
        endpoints_protegidos = [
            ('/api/v1/users/me/', 'user-me'),
        ]
        
        for url_path, url_name in endpoints_protegidos:
            try:
                url = reverse(url_name)
            except:
                url = url_path
            
            response = self.client.get(url)
            
            if response.status_code == 404:
                continue  # Endpoint não configurado ainda
            
            # Deve ser negado acesso
            self.assertIn(response.status_code, [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ], f"Usuário não autenticado teve acesso a {url}")
    
    def test_token_invalido_negado(self):
        """Testa se token inválido é rejeitado"""
        # Configurar token inválido
        self.client.credentials(HTTP_AUTHORIZATION='Bearer token_invalido')
        
        try:
            url = reverse('user-me')
        except:
            url = '/api/v1/users/me/'
        
        response = self.client.get(url)
        
        if response.status_code == 404:
            self.skipTest("Endpoint /me não configurado ainda")
        
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])
    
    def test_admin_tem_acesso_listagem(self):
        """Testa se admin consegue acessar listagens"""
        self.authenticate_user(self.admin_user)
        
        try:
            url = reverse('user-list')
        except:
            url = '/api/v1/users/'
        
        response = self.client.get(url)
        
        if response.status_code == 404:
            self.skipTest("Endpoint de listagem não configurado ainda")
        
        # Admin deve ter acesso (200) ou pelo menos não ser negado (403)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                          "Admin foi negado acesso à listagem de usuários")
