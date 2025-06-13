#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitTrack.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Perfil

def create_admin_user():
    # Criar usuário admin se não existir
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fittrack.com',
            'is_staff': True,
            'is_superuser': True
        }
    )

    if created:
        user.set_password('admin123')
        user.save()
        print('✅ Usuário admin criado!')
    else:
        print('ℹ️ Usuário admin já existe')

    # Verificar/atualizar perfil
    try:
        perfil = user.perfil
        if perfil.tipo != 'admin':
            perfil.tipo = 'admin'
            perfil.save()
            print('✅ Perfil atualizado para admin')
        else:
            print('ℹ️ Perfil já é admin')
    except Exception as e:
        print(f'⚠️ Erro ao verificar perfil: {e}')

    print(f'\n📋 Informações do usuário:')
    print(f'   Username: {user.username}')
    print(f'   Email: {user.email}')
    print(f'   Is Staff: {user.is_staff}')
    print(f'   Password set: {user.has_usable_password()}')
    
    if hasattr(user, 'perfil'):
        print(f'   Perfil tipo: {user.perfil.tipo}')
        print(f'   Perfil ID: {user.perfil.id}')
    else:
        print('   ⚠️ Sem perfil associado')

if __name__ == '__main__':
    create_admin_user()