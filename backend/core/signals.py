from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil, Cliente, Personal, Nutricionista


@receiver(post_save, sender=Perfil)
def create_related_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente o objeto relacionado (Cliente, Personal ou Nutricionista)
    quando um Perfil é criado.
    """
    if created or not hasattr(instance, 'get_related_object'):
        try:
            if instance.tipo == 'cliente':
                # Verifica se já não existe um Cliente para este perfil
                if not Cliente.objects.filter(perfil=instance).exists():
                    Cliente.objects.create(
                        perfil=instance,
                        nome=f"{instance.usuario.first_name} {instance.usuario.last_name}".strip() or instance.usuario.username,
                        email=instance.usuario.email
                    )
                    print(f"Cliente criado para perfil: {instance.usuario.username}")
                    
            elif instance.tipo == 'personal':
                # Verifica se já não existe um Personal para este perfil
                if not Personal.objects.filter(perfil=instance).exists():
                    Personal.objects.create(
                        perfil=instance,
                        nome=f"{instance.usuario.first_name} {instance.usuario.last_name}".strip() or instance.usuario.username,
                        email=instance.usuario.email,
                        especialidade="Personal Trainer"
                    )
                    print(f"Personal criado para perfil: {instance.usuario.username}")
                    
            elif instance.tipo == 'nutricionista':
                # Verifica se já não existe um Nutricionista para este perfil
                if not Nutricionista.objects.filter(perfil=instance).exists():
                    Nutricionista.objects.create(
                        perfil=instance,
                        nome=f"{instance.usuario.first_name} {instance.usuario.last_name}".strip() or instance.usuario.username,
                        email=instance.usuario.email,
                        especialidade="Nutrição Esportiva"
                    )
                    print(f"Nutricionista criado para perfil: {instance.usuario.username}")
        except Exception as e:
            print(f"Erro ao criar objeto relacionado para perfil {instance.usuario.username}: {str(e)}")


@receiver(post_save, sender=User)
def create_perfil_for_user(sender, instance, created, **kwargs):
    """
    Cria automaticamente um Perfil quando um User é criado.
    Por padrão, cria como 'cliente' a menos que seja staff.
    """
    if created:
        # Verifica se já existe um perfil para este usuário
        if not Perfil.objects.filter(usuario=instance).exists():
            tipo = 'admin' if instance.is_staff else 'cliente'
            Perfil.objects.create(
                usuario=instance,
                tipo=tipo
            )
            print(f"Perfil criado para usuário: {instance.username} com tipo: {tipo}")
        else:
            print(f"Perfil já existe para usuário: {instance.username}")