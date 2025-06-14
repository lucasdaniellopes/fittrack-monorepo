# Generated by Django 5.1.7 on 2025-03-31 22:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_cliente_data_ultima_dieta_cliente_data_ultimo_treino_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('admin', 'Administrador'), ('nutricionista', 'Nutricionista'), ('personal', 'Personal Trainer'), ('cliente', 'Cliente')], default='cliente', max_length=20)),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='perfil',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='core.perfil'),
        ),
    ]
