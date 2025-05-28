from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Perfil, Cliente


class Command(BaseCommand):
    help = 'Create Cliente objects for perfils with tipo=cliente that don\'t have one'

    def handle(self, *args, **options):
        # Find all perfils with tipo='cliente' that don't have a Cliente
        perfis_sem_cliente = Perfil.objects.filter(
            tipo='cliente',
            cliente__isnull=True
        )
        
        created_count = 0
        for perfil in perfis_sem_cliente:
            # Create a Cliente for this perfil
            cliente = Cliente.objects.create(
                nome=f"{perfil.usuario.first_name} {perfil.usuario.last_name}".strip() or perfil.usuario.username,
                email=perfil.usuario.email,
                perfil=perfil
            )
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created Cliente for user {perfil.usuario.username}'
                )
            )
        
        if created_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All cliente perfils already have Cliente objects')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Created {created_count} Cliente objects')
            )