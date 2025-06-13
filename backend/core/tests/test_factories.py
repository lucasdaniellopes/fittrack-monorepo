from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil
from core.factories.profile_factory import ProfileFactoryRegistry


class ProfileFactoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='factory_test',
            email='factory@test.com',
            password='testpass123'
        )
        # Obter o perfil criado automaticamente pelos signals
        self.perfil = Perfil.objects.get(usuario=self.user)
    
    def test_cliente_profile_factory(self):
        # Atualizar o tipo do perfil para cliente
        self.perfil.tipo = Perfil.CLIENTE
        self.perfil.save()
        
        profile_instance = ProfileFactoryRegistry.create_profile(self.perfil)
        self.assertIsNotNone(profile_instance)
        self.assertEqual(profile_instance.perfil, self.perfil)
    
    def test_personal_profile_factory(self):
        # Atualizar o tipo do perfil para personal
        self.perfil.tipo = Perfil.PERSONAL
        self.perfil.save()
        
        profile_instance = ProfileFactoryRegistry.create_profile(self.perfil)
        self.assertIsNotNone(profile_instance)
        self.assertEqual(profile_instance.perfil, self.perfil)
    
    def test_nutricionista_profile_factory(self):
        # Atualizar o tipo do perfil para nutricionista
        self.perfil.tipo = Perfil.NUTRICIONISTA
        self.perfil.save()
        
        profile_instance = ProfileFactoryRegistry.create_profile(self.perfil)
        self.assertIsNotNone(profile_instance)
        self.assertEqual(profile_instance.perfil, self.perfil)