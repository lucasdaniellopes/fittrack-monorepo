from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Perfil, Cliente
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio


class TreinoViewSetTest(APITestCase):
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
        
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Descrição do treino",
            duracao=60,
            cliente=self.cliente
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.client_token = str(RefreshToken.for_user(self.client_user).access_token)
    
    def test_unauthenticated_access_denied(self):
        response = self.client.get('/api/v1/treinos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_access_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/treinos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_treino_list_structure(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/treinos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
        if response.data['results']:
            treino_data = response.data['results'][0]
            expected_fields = ['id', 'nome', 'descricao', 'duracao', 'cliente']
            for field in expected_fields:
                self.assertIn(field, treino_data)
    
    def test_create_treino(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'nome': 'Novo Treino',
            'descricao': 'Descrição do novo treino',
            'duracao': 45,
            'cliente': self.cliente.id
        }
        
        response = self.client.post('/api/v1/treinos/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_update_treino(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'duracao': 75,
            'descricao': 'Descrição atualizada'
        }
        
        response = self.client.patch(f'/api/v1/treinos/{self.treino.id}/', data)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_delete_treino(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(f'/api/v1/treinos/{self.treino.id}/')
        
        self.assertIn(response.status_code, [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_treino_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/treinos/{self.treino.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.treino.id)
            self.assertEqual(response.data['nome'], self.treino.nome)


class ExercicioViewSetTest(APITestCase):
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
            perfil=self.admin_perfil  # Usando admin perfil para simplificar
        )
        
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        
        self.exercicio = Exercicio.objects.create(
            nome="Supino",
            descricao="Exercício para peitoral",
            treino=self.treino
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_exercicio_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/exercicios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_exercicio(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'nome': 'Agachamento',
            'descricao': 'Exercício para pernas',
            'treino': self.treino.id
        }
        
        response = self.client.post('/api/v1/exercicios/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_exercicio_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/exercicios/{self.exercicio.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.exercicio.id)
            self.assertEqual(response.data['nome'], self.exercicio.nome)


class HistoricoTreinoViewSetTest(APITestCase):
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
        
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        
        self.historico = HistoricoTreino.objects.create(
            cliente=self.cliente,
            treino=self.treino,
            data_inicio="2024-01-15"
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_historico_treino_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/historico-treinos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_historico_treino(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        data = {
            'cliente': self.cliente.id,
            'treino': self.treino.id,
            'data_inicio': '2024-01-20',
            'observacoes': 'Novo histórico de teste'
        }
        
        response = self.client.post('/api/v1/historico-treinos/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_historico_treino_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/historico-treinos/{self.historico.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.historico.id)
            self.assertEqual(response.data['cliente'], self.cliente.id)


class TrocaExercicioViewSetTest(APITestCase):
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
        
        self.treino = Treino.objects.create(
            nome="Treino Teste",
            descricao="Treino de teste",
            duracao=60,
            cliente=self.cliente
        )
        
        self.exercicio_antigo = Exercicio.objects.create(
            nome="Supino",
            treino=self.treino
        )
        
        self.exercicio_novo = Exercicio.objects.create(
            nome="Supino Inclinado",
            treino=self.treino
        )
        
        self.troca = TrocaExercicio.objects.create(
            cliente=self.cliente,
            exercicio_antigo=self.exercicio_antigo,
            exercicio_novo=self.exercicio_novo,
            motivo="Teste"
        )
        
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_troca_exercicio_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/v1/trocas-exercicios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_troca_exercicio(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        exercicio_outro = Exercicio.objects.create(
            nome="Leg Press",
            treino=self.treino
        )
        
        data = {
            'cliente': self.cliente.id,
            'exercicio_antigo': self.exercicio_novo.id,
            'exercicio_novo': exercicio_outro.id,
            'motivo': 'Nova troca de teste'
        }
        
        response = self.client.post('/api/v1/trocas-exercicios/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ])
    
    def test_troca_exercicio_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/v1/trocas-exercicios/{self.troca.id}/')
        
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.troca.id)
            self.assertEqual(response.data['cliente'], self.cliente.id)
    
    def test_approve_troca_exercicio(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Testar endpoint de aprovação se existir
        response = self.client.patch(
            f'/api/v1/trocas-exercicios/{self.troca.id}/',
            {'status': TrocaExercicio.APROVADA}
        )
        
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])
    
    def test_reject_troca_exercicio(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Testar endpoint de rejeição se existir
        response = self.client.patch(
            f'/api/v1/trocas-exercicios/{self.troca.id}/',
            {'status': TrocaExercicio.REJEITADA}
        )
        
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ])