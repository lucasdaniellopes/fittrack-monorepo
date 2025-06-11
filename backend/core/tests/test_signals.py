from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from core.models import Perfil
from core.signals import create_perfil_for_user


class PerfilSignalTest(TestCase):
    """Testes para os signals do Perfil"""
    
    def test_signal_cria_perfil_para_usuario_comum(self):
        """Testa se o signal cria perfil 'cliente' para usuário comum"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Verificar se o perfil foi criado automaticamente
        self.assertTrue(Perfil.objects.filter(usuario=user).exists())
        
        perfil = Perfil.objects.get(usuario=user)
        self.assertEqual(perfil.tipo, 'cliente')
        self.assertEqual(perfil.usuario, user)
    
    def test_signal_cria_perfil_para_usuario_staff(self):
        """Testa se o signal cria perfil 'admin' para usuário staff"""
        staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        
        # Verificar se o perfil foi criado automaticamente
        self.assertTrue(Perfil.objects.filter(usuario=staff_user).exists())
        
        perfil = Perfil.objects.get(usuario=staff_user)
        self.assertEqual(perfil.tipo, 'admin')
        self.assertEqual(perfil.usuario, staff_user)
    
    def test_signal_nao_cria_perfil_duplicado(self):
        """Testa se o signal não cria perfil duplicado"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Verificar se existe apenas um perfil
        perfis_count = Perfil.objects.filter(usuario=user).count()
        self.assertEqual(perfis_count, 1)
        
        # Tentar "salvar" o usuário novamente (simular signal)
        user.save()
        
        # Ainda deve haver apenas um perfil
        perfis_count = Perfil.objects.filter(usuario=user).count()
        self.assertEqual(perfis_count, 1)
    
    def test_signal_funciona_com_superuser(self):
        """Testa se o signal funciona corretamente com superuser"""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Verificar se o perfil foi criado
        self.assertTrue(Perfil.objects.filter(usuario=superuser).exists())
        
        perfil = Perfil.objects.get(usuario=superuser)
        # Superuser é staff, então deve ser admin
        self.assertEqual(perfil.tipo, 'admin')
    
    def test_signal_conectado_corretamente(self):
        """Testa se o signal está conectado ao modelo User"""
        # Teste funcional: criar um usuário e verificar se o signal funciona
        test_user = User.objects.create_user(
            username='signal_test_user',
            email='signal_test@example.com',
            password='testpass123'
        )
        
        # Se o perfil foi criado automaticamente, o signal está funcionando
        perfil_exists = Perfil.objects.filter(usuario=test_user).exists()
        self.assertTrue(perfil_exists, "Signal não está funcionando - perfil não foi criado automaticamente")
        
        # Verificar se o perfil tem o tipo correto
        if perfil_exists:
            perfil = Perfil.objects.get(usuario=test_user)
            self.assertEqual(perfil.tipo, 'cliente')
        
        # Limpar o usuário de teste
        test_user.delete()

