from abc import ABC, abstractmethod
from typing import Dict, Any


class ProfileFactory(ABC):
    """Abstract factory for creating profile-specific instances"""
    
    @abstractmethod
    def create_profile(self, perfil_instance) -> Any:
        """Create a profile-specific instance based on perfil"""
        pass
    
    @abstractmethod
    def get_default_data(self, perfil_instance) -> Dict[str, Any]:
        """Get default data for the profile type"""
        pass


class ClienteProfileFactory(ProfileFactory):
    """Factory for creating Cliente instances"""
    
    def create_profile(self, perfil_instance):
        from accounts.models import Cliente
        
        default_data = self.get_default_data(perfil_instance)
        return Cliente.objects.create(**default_data)
    
    def get_default_data(self, perfil_instance) -> Dict[str, Any]:
        return {
            'perfil': perfil_instance,
            'nome': self._get_full_name(perfil_instance),
            'email': perfil_instance.usuario.email,
            'trocas_exercicios_restantes': 0,
            'trocas_refeicoes_restantes': 0,
        }
    
    def _get_full_name(self, perfil_instance) -> str:
        user = perfil_instance.usuario
        if user.first_name or user.last_name:
            return f"{user.first_name} {user.last_name}".strip()
        return user.username


class PersonalProfileFactory(ProfileFactory):
    """Factory for creating Personal instances"""
    
    def create_profile(self, perfil_instance):
        from accounts.models import Personal
        
        default_data = self.get_default_data(perfil_instance)
        return Personal.objects.create(**default_data)
    
    def get_default_data(self, perfil_instance) -> Dict[str, Any]:
        return {
            'perfil': perfil_instance,
            'nome': self._get_full_name(perfil_instance),
            'email': perfil_instance.usuario.email,
            'especialidade': '',
        }
    
    def _get_full_name(self, perfil_instance) -> str:
        user = perfil_instance.usuario
        if user.first_name or user.last_name:
            return f"{user.first_name} {user.last_name}".strip()
        return user.username


class NutricionistaProfileFactory(ProfileFactory):
    """Factory for creating Nutricionista instances"""
    
    def create_profile(self, perfil_instance):
        from accounts.models import Nutricionista
        
        default_data = self.get_default_data(perfil_instance)
        return Nutricionista.objects.create(**default_data)
    
    def get_default_data(self, perfil_instance) -> Dict[str, Any]:
        return {
            'perfil': perfil_instance,
            'nome': self._get_full_name(perfil_instance),
            'email': perfil_instance.usuario.email,
            'especialidade': '',
            'crn': '',
        }
    
    def _get_full_name(self, perfil_instance) -> str:
        user = perfil_instance.usuario
        if user.first_name or user.last_name:
            return f"{user.first_name} {user.last_name}".strip()
        return user.username


class ProfileFactoryRegistry:
    """Registry to manage and provide profile factories"""
    
    _factories = {
        'cliente': ClienteProfileFactory(),
        'personal': PersonalProfileFactory(),
        'nutricionista': NutricionistaProfileFactory(),
    }
    
    @classmethod
    def create_profile(cls, perfil_instance):
        """Create appropriate profile instance based on perfil type"""
        factory = cls._factories.get(perfil_instance.tipo)
        if factory:
            try:
                return factory.create_profile(perfil_instance)
            except Exception as e:
                print(f"Error creating profile for {perfil_instance.tipo}: {str(e)}")
                return None
        else:
            print(f"No factory found for profile type: {perfil_instance.tipo}")
            return None
    
    @classmethod
    def register_factory(cls, profile_type: str, factory: ProfileFactory):
        """Register a new factory for a profile type"""
        cls._factories[profile_type] = factory
    
    @classmethod
    def get_factory(cls, profile_type: str) -> ProfileFactory:
        """Get factory for a specific profile type"""
        return cls._factories.get(profile_type)