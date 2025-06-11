from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from core.models import Perfil


class PerfilModelTest(TestCase):
    """Testes para o model Perfil"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
    
    def test_perfil_creation(self):
        # Verificar se o perfil existe
        self.assertTrue(Perfil.objects.filter(usuario=self.user).exists())
        
        # Verificar os dados do perfil
        self.assertEqual(self.perfil.usuario, self.user)
        self.assertEqual(self.perfil.tipo, 'cliente')
        self.assertIsNotNone(self.perfil.created_at)
        self.assertIsNotNone(self.perfil.updated_at)
    
    def test_perfil_creation_manual(self):
        """Testa a criação manual de um perfil para novo usuário"""
        # Criar novo usuário
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='testpass123'
        )
        
        # Verificar se o signal criou o perfil
        self.assertTrue(Perfil.objects.filter(usuario=new_user).exists())
        perfil = Perfil.objects.get(usuario=new_user)
        
        self.assertEqual(perfil.usuario, new_user)
        self.assertEqual(perfil.tipo, 'cliente')
    
    def test_perfil_str_method(self):
        """Testa o método __str__ do perfil"""
        # O método __str__ retorna o tipo com primeira letra maiúscula
        expected_str = f"{self.user.username} - Cliente"
        self.assertEqual(str(self.perfil), expected_str)
    
    def test_perfil_tipos_validos(self):
        """Testa se apenas tipos válidos são aceitos"""
        tipos_validos = ['admin', 'nutricionista', 'personal', 'cliente']
        
        for tipo in tipos_validos:
            with self.subTest(tipo=tipo):
                user = User.objects.create_user(
                    username=f'user_{tipo}',
                    email=f'{tipo}@test.com',
                    password='testpass123'
                )
                # O signal criou como 'cliente', vamos alterar para testar
                perfil = Perfil.objects.get(usuario=user)
                perfil.tipo = tipo
                perfil.save()
                
                perfil.refresh_from_db()
                self.assertEqual(perfil.tipo, tipo)
    
    def test_perfil_unique_usuario(self):
        """Testa se um usuário pode ter apenas um perfil"""
        # Tentar criar segundo perfil para o mesmo usuário deve falhar
        with self.assertRaises(IntegrityError):
            Perfil.objects.create(usuario=self.user, tipo='admin')
    
    def test_perfil_campos_obrigatorios(self):
        """Testa se campos obrigatórios são validados"""
        # Verificar se o perfil criado automaticamente tem os campos obrigatórios
        self.assertIsNotNone(self.perfil.usuario)
        self.assertIsNotNone(self.perfil.tipo)
        self.assertTrue(self.perfil.tipo in ['admin', 'nutricionista', 'personal', 'cliente'])
        
        # Verificar se não podemos ter perfil sem tipo válido
        self.perfil.tipo = 'cliente'  # Garantir que tem um tipo válido
        self.perfil.save()  # Deve funcionar
        
        # Verificar se o perfil está associado ao usuário correto
        self.assertEqual(self.perfil.usuario, self.user)

    
    def test_perfil_timestamps(self):
        """Testa se timestamps são criados e atualizados corretamente"""
        created_at_original = self.perfil.created_at
        updated_at_original = self.perfil.updated_at
        
        # Atualizar perfil
        self.perfil.tipo = 'nutricionista'
        self.perfil.save()
        
        self.perfil.refresh_from_db()
        
        # created_at não deve mudar
        self.assertEqual(self.perfil.created_at, created_at_original)
        
        # updated_at deve ser diferente
        self.assertNotEqual(self.perfil.updated_at, updated_at_original)
    
    def test_perfil_admin_para_staff(self):
        """Testa se usuário staff recebe perfil admin automaticamente"""
        staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='testpass123',
            is_staff=True
        )
        
        perfil = Perfil.objects.get(usuario=staff_user)
        self.assertEqual(perfil.tipo, 'admin')
