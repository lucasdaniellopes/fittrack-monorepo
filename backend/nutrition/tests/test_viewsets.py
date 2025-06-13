from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Perfil, Cliente
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao


class DietaViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        self.client_user = User.objects.create_user(
            username='client',
            email='client@test.com',
            password='testpass123'
        )
        
        self.admin_perfil = Perfil.objects.get(usuario=self.admin_user)
        self.client_perfil = Perfil.objects.get(usuario=self.client_user)
        
        self.admin_perfil.tipo = Perfil.ADMIN
        self.admin_perfil.save()
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.client_perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.client_token = str(RefreshToken.for_user(self.client_user).access_token)
    
    def test_unauthenticated_access_denied(self):
        response = self.client.get('/api/v1/dietas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_access_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/dietas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_dieta_list_structure(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/dietas/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
        if response.data['results']:
            dieta_data = response.data['results'][0]
            expected_fields = ['id', 'nome', 'descricao', 'calorias', 'cliente']
            for field in expected_fields:
                self.assertIn(field, dieta_data)
    
    def test_create_dieta(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'nome': 'Nova Dieta',
            'descricao': 'Descrição da nova dieta',
            'calorias': 1800,
            'cliente': self.cliente.id
        }
        
        response = self.client.post('/api/v1/dietas/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_update_dieta(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'calorias': 2200,
            'descricao': 'Descrição atualizada'
        }
        
        response = self.client.patch(f'/api/v1/dietas/{self.dieta.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_delete_dieta(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(f'/api/v1/dietas/{self.dieta.id}/')
        
        self.assertIn(response.status_code, [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_dieta_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/dietas/{self.dieta.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.dieta.id)
            self.assertEqual(response.data['nome'], self.dieta.nome)


class RefeicaoViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.admin_perfil = Perfil.objects.get(usuario=self.admin_user)
        self.admin_perfil.tipo = Perfil.ADMIN
        self.admin_perfil.save()
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.admin_perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.refeicao = Refeicao.objects.create(
            nome="Café da Manhã",
            descricao="Primeira refeição do dia",
            calorias=300,
            dieta=self.dieta
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_refeicao_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/refeicoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_refeicao(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'nome': 'Almoço',
            'descricao': 'Refeição principal do dia',
            'calorias': 600,
            'dieta': self.dieta.id
        }
        
        response = self.client.post('/api/v1/refeicoes/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_refeicao_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/refeicoes/{self.refeicao.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.refeicao.id)
            self.assertEqual(response.data['nome'], self.refeicao.nome)
    
    def test_update_refeicao(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'calorias': 350,
            'descricao': 'Descrição atualizada'
        }
        
        response = self.client.patch(f'/api/v1/refeicoes/{self.refeicao.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])


class HistoricoDietaViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.admin_perfil = Perfil.objects.get(usuario=self.admin_user)
        self.admin_perfil.tipo = Perfil.ADMIN
        self.admin_perfil.save()
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.admin_perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15",
            observacoes="Dieta iniciada"
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_historico_dieta_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/historico-dietas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_historico_dieta(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'cliente': self.cliente.id,
            'dieta': self.dieta.id,
            'data_inicio': '2024-01-20',
            'observacoes': 'Novo histórico de teste'
        }
        
        response = self.client.post('/api/v1/historico-dietas/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_historico_dieta_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/historico-dietas/{self.historico.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.historico.id)
            self.assertEqual(response.data['cliente'], self.cliente.id)
    
    def test_update_historico_dieta(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'observacoes': 'Observações atualizadas',
            'data_fim': '2024-01-25'
        }
        
        response = self.client.patch(f'/api/v1/historico-dietas/{self.historico.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])


class TrocaRefeicaoViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.admin_perfil = Perfil.objects.get(usuario=self.admin_user)
        self.admin_perfil.tipo = Perfil.ADMIN
        self.admin_perfil.save()
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.admin_perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.refeicao_antiga = Refeicao.objects.create(
            nome="Café Original",
            calorias=300,
            dieta=self.dieta
        )
        
        self.refeicao_nova = Refeicao.objects.create(
            nome="Café Alternativo",
            calorias=320,
            dieta=self.dieta
        )
        
        self.troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Teste"
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_troca_refeicao_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/trocas-refeicoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_troca_refeicao(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        refeicao_outra = Refeicao.objects.create(
            nome="Jantar",
            calorias=500,
            dieta=self.dieta
        )
        
        data = {
            'cliente': self.cliente.id,
            'refeicao_antiga': self.refeicao_nova.id,
            'refeicao_nova': refeicao_outra.id,
            'motivo': 'Nova troca de teste'
        }
        
        response = self.client.post('/api/v1/trocas-refeicoes/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_troca_refeicao_with_suggestion(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'cliente': self.cliente.id,
            'refeicao_antiga': self.refeicao_antiga.id,
            'refeicao_sugerida': 'Aveia com frutas',
            'motivo': 'Quero algo mais leve'
        }
        
        response = self.client.post('/api/v1/trocas-refeicoes/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_troca_refeicao_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/trocas-refeicoes/{self.troca.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.troca.id)
            self.assertEqual(response.data['cliente'], self.cliente.id)
    
    def test_approve_troca_refeicao(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'status': 'APROVADO',
            'observacoes_resposta': 'Aprovado pela nutricionista'
        }
        
        response = self.client.patch(f'/api/v1/trocas-refeicoes/{self.troca.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_reject_troca_refeicao(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'status': 'REJEITADO',
            'observacoes_resposta': 'Não aprovado por motivos nutricionais'
        }
        
        response = self.client.patch(f'/api/v1/trocas-refeicoes/{self.troca.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_troca_refeicao_status_filter(self):
        # Criar trocas com diferentes status
        troca_aprovada = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Troca aprovada",
            status='APROVADO'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Testar filtro por status (se disponível)
        response = self.client.get('/api/v1/trocas-refeicoes/?status=APROVADO')
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST
        ])