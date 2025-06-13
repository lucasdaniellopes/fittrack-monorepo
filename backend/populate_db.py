#!/usr/bin/env python
import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitTrack.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente, Personal, Nutricionista
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao

def create_users():
    print("👥 Criando usuários...")
    
    # Admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fittrack.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    admin_user.perfil.tipo = 'admin'
    admin_user.perfil.save()
    
    # Personal Trainer
    personal_user, created = User.objects.get_or_create(
        username='carlos_personal',
        defaults={
            'email': 'carlos@fittrack.com',
            'first_name': 'Carlos',
            'last_name': 'Silva',
            'password': 'personal123'
        }
    )
    if created:
        personal_user.set_password('personal123')
        personal_user.save()
    personal_user.perfil.tipo = 'personal'
    personal_user.perfil.telefone = '(11) 99999-1111'
    personal_user.perfil.save()
    
    # Nutricionista
    nutri_user, created = User.objects.get_or_create(
        username='ana_nutri',
        defaults={
            'email': 'ana@fittrack.com',
            'first_name': 'Ana',
            'last_name': 'Costa',
            'password': 'nutri123'
        }
    )
    if created:
        nutri_user.set_password('nutri123')
        nutri_user.save()
    nutri_user.perfil.tipo = 'nutricionista'
    nutri_user.perfil.telefone = '(11) 99999-2222'
    nutri_user.perfil.save()
    
    # Clientes
    clientes_data = [
        ('joao_cliente', 'joao@gmail.com', 'João', 'Santos'),
        ('maria_cliente', 'maria@gmail.com', 'Maria', 'Oliveira'),
        ('pedro_cliente', 'pedro@gmail.com', 'Pedro', 'Lima'),
        ('ana_cliente', 'ana.cliente@gmail.com', 'Ana', 'Ferreira'),
    ]
    
    for username, email, first_name, last_name in clientes_data:
        client_user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': 'cliente123'
            }
        )
        if created:
            client_user.set_password('cliente123')
            client_user.save()
        client_user.perfil.tipo = 'cliente'
        client_user.perfil.save()
    
    print(f"✅ Usuários criados/verificados")

def create_tipo_planos():
    print("💳 Criando tipos de plano...")
    
    planos_data = [
        {
            'nome': 'Plano Básico',
            'descricao': 'Plano ideal para iniciantes',
            'preco': '99.90',
            'duracao_dias': 30,
            'limite_trocas_exercicios': 3,
            'limite_trocas_refeicoes': 2,
            'periodo_trocas_dias': 7
        },
        {
            'nome': 'Plano Premium',
            'descricao': 'Plano completo com mais benefícios',
            'preco': '199.90',
            'duracao_dias': 30,
            'limite_trocas_exercicios': 8,
            'limite_trocas_refeicoes': 5,
            'periodo_trocas_dias': 3
        },
        {
            'nome': 'Plano VIP',
            'descricao': 'Plano com trocas ilimitadas',
            'preco': '299.90',
            'duracao_dias': 30,
            'trocas_ilimitadas': True,
            'periodo_trocas_dias': 1
        }
    ]
    
    for plano_data in planos_data:
        TipoPlano.objects.get_or_create(
            nome=plano_data['nome'],
            defaults=plano_data
        )
    
    print(f"✅ {len(planos_data)} tipos de plano criados")

def create_profiles():
    print("👤 Criando perfis profissionais...")
    
    # Personal Trainer
    personal_user = User.objects.get(username='carlos_personal')
    Personal.objects.get_or_create(
        perfil=personal_user.perfil,
        defaults={
            'nome': f"{personal_user.first_name} {personal_user.last_name}",
            'email': personal_user.email,
            'telefone': '(11) 99999-1111',
            'especialidade': 'Musculação e Condicionamento Físico'
        }
    )
    
    # Nutricionista
    nutri_user = User.objects.get(username='ana_nutri')
    Nutricionista.objects.get_or_create(
        perfil=nutri_user.perfil,
        defaults={
            'nome': f"{nutri_user.first_name} {nutri_user.last_name}",
            'email': nutri_user.email,
            'telefone': '(11) 99999-2222',
            'especialidade': 'Nutrição Esportiva',
            'crn': 'CRN-3/12345'
        }
    )
    
    print("✅ Perfis profissionais criados")

def create_clientes():
    print("👥 Criando clientes...")
    
    plano_basico = TipoPlano.objects.get(nome='Plano Básico')
    plano_premium = TipoPlano.objects.get(nome='Plano Premium')
    plano_vip = TipoPlano.objects.get(nome='Plano VIP')
    
    clientes_data = [
        {
            'username': 'joao_cliente',
            'nome': 'João Santos',
            'email': 'joao@gmail.com',
            'telefone': '(11) 99999-3333',
            'altura': 175,
            'peso': 80,
            'tipo_plano': plano_premium,
            'data_nascimento': date(1990, 5, 15)
        },
        {
            'username': 'maria_cliente',
            'nome': 'Maria Oliveira',
            'email': 'maria@gmail.com',
            'telefone': '(11) 99999-4444',
            'altura': 165,
            'peso': 65,
            'tipo_plano': plano_basico,
            'data_nascimento': date(1988, 8, 22)
        },
        {
            'username': 'pedro_cliente',
            'nome': 'Pedro Lima',
            'email': 'pedro@gmail.com',
            'telefone': '(11) 99999-5555',
            'altura': 180,
            'peso': 90,
            'tipo_plano': plano_vip,
            'data_nascimento': date(1992, 3, 10)
        },
        {
            'username': 'ana_cliente',
            'nome': 'Ana Ferreira',
            'email': 'ana.cliente@gmail.com',
            'telefone': '(11) 99999-6666',
            'altura': 160,
            'peso': 55,
            'tipo_plano': plano_premium,
            'data_nascimento': date(1995, 12, 5)
        }
    ]
    
    for cliente_data in clientes_data:
        user = User.objects.get(username=cliente_data['username'])
        user.perfil.telefone = cliente_data['telefone']
        user.perfil.data_nascimento = cliente_data['data_nascimento']
        user.perfil.save()
        
        Cliente.objects.get_or_create(
            perfil=user.perfil,
            defaults={
                'nome': cliente_data['nome'],
                'email': cliente_data['email'],
                'telefone': cliente_data['telefone'],
                'altura': cliente_data['altura'],
                'peso': cliente_data['peso'],
                'tipo_plano': cliente_data['tipo_plano'],
                'data_nascimento': cliente_data['data_nascimento'],
                'data_inicio_plano': date.today() - timedelta(days=15),
                'data_fim_plano': date.today() + timedelta(days=15)
            }
        )
    
    print(f"✅ {len(clientes_data)} clientes criados")

def create_treinos():
    print("💪 Criando treinos...")
    
    clientes = Cliente.objects.all()
    
    treinos_data = [
        {
            'nome': 'Treino Push - Peito, Ombro e Tríceps',
            'descricao': 'Treino focado em movimentos de empurrar',
            'duracao': 60,
            'exercicios': [
                {'nome': 'Supino Reto', 'descricao': '4x12 - Peitorais'},
                {'nome': 'Supino Inclinado', 'descricao': '3x10 - Parte superior do peitoral'},
                {'nome': 'Desenvolvimento', 'descricao': '4x12 - Ombros'},
                {'nome': 'Elevação Lateral', 'descricao': '3x15 - Deltóide lateral'},
                {'nome': 'Tríceps Testa', 'descricao': '3x12 - Tríceps'},
                {'nome': 'Tríceps Corda', 'descricao': '3x15 - Tríceps'}
            ]
        },
        {
            'nome': 'Treino Pull - Costas e Bíceps',
            'descricao': 'Treino focado em movimentos de puxar',
            'duracao': 55,
            'exercicios': [
                {'nome': 'Puxada Frontal', 'descricao': '4x12 - Latíssimo do dorso'},
                {'nome': 'Remada Curvada', 'descricao': '4x10 - Rombóides e trapézio'},
                {'nome': 'Puxada Triangular', 'descricao': '3x12 - Latíssimo'},
                {'nome': 'Rosca Direta', 'descricao': '4x12 - Bíceps'},
                {'nome': 'Rosca Martelo', 'descricao': '3x15 - Bíceps e antebraço'}
            ]
        },
        {
            'nome': 'Treino Legs - Pernas',
            'descricao': 'Treino completo de membros inferiores',
            'duracao': 70,
            'exercicios': [
                {'nome': 'Agachamento Livre', 'descricao': '4x12 - Quadríceps e glúteos'},
                {'nome': 'Leg Press 45°', 'descricao': '4x15 - Quadríceps'},
                {'nome': 'Stiff', 'descricao': '4x12 - Posterior de coxa'},
                {'nome': 'Mesa Flexora', 'descricao': '3x15 - Posterior de coxa'},
                {'nome': 'Panturrilha Sentado', 'descricao': '4x20 - Panturrilhas'},
                {'nome': 'Panturrilha em Pé', 'descricao': '3x15 - Panturrilhas'}
            ]
        }
    ]
    
    for cliente in clientes:
        for treino_data in treinos_data:
            treino, created = Treino.objects.get_or_create(
                nome=treino_data['nome'],
                cliente=cliente,
                defaults={
                    'descricao': treino_data['descricao'],
                    'duracao': treino_data['duracao']
                }
            )
            
            if created:
                for exercicio_data in treino_data['exercicios']:
                    Exercicio.objects.create(
                        nome=exercicio_data['nome'],
                        descricao=exercicio_data['descricao'],
                        treino=treino
                    )
    
    print(f"✅ Treinos criados para {clientes.count()} clientes")

def create_dietas():
    print("🥗 Criando dietas...")
    
    clientes = Cliente.objects.all()
    
    dietas_data = [
        {
            'nome': 'Dieta para Ganho de Massa',
            'descricao': 'Dieta hipercalórica para ganho de massa muscular',
            'calorias': 2800,
            'refeicoes': [
                {'nome': 'Café da Manhã', 'descricao': '2 ovos, 2 fatias de pão integral, 1 banana', 'calorias': 450},
                {'nome': 'Lanche da Manhã', 'descricao': 'Whey protein com leite', 'calorias': 300},
                {'nome': 'Almoço', 'descricao': 'Frango grelhado, arroz integral, feijão, salada', 'calorias': 800},
                {'nome': 'Lanche da Tarde', 'descricao': 'Sanduíche de peito de peru', 'calorias': 400},
                {'nome': 'Pré-treino', 'descricao': 'Banana com aveia', 'calorias': 250},
                {'nome': 'Pós-treino', 'descricao': 'Whey protein com dextrose', 'calorias': 350},
                {'nome': 'Jantar', 'descricao': 'Salmão, batata doce, brócolis', 'calorias': 600}
            ]
        },
        {
            'nome': 'Dieta para Emagrecimento',
            'descricao': 'Dieta hipocalórica para perda de peso',
            'calorias': 1600,
            'refeicoes': [
                {'nome': 'Café da Manhã', 'descricao': 'Omelete de claras, 1 fatia de pão integral', 'calorias': 250},
                {'nome': 'Lanche da Manhã', 'descricao': 'Fruta da estação', 'calorias': 80},
                {'nome': 'Almoço', 'descricao': 'Peito de frango, salada verde, quinoa', 'calorias': 450},
                {'nome': 'Lanche da Tarde', 'descricao': 'Iogurte natural com chia', 'calorias': 150},
                {'nome': 'Pré-treino', 'descricao': 'Maçã pequena', 'calorias': 80},
                {'nome': 'Jantar', 'descricao': 'Peixe grelhado com legumes', 'calorias': 400},
                {'nome': 'Ceia', 'descricao': 'Chá verde', 'calorias': 5}
            ]
        }
    ]
    
    for cliente in clientes:
        for dieta_data in dietas_data:
            dieta, created = Dieta.objects.get_or_create(
                nome=dieta_data['nome'],
                cliente=cliente,
                defaults={
                    'descricao': dieta_data['descricao'],
                    'calorias': dieta_data['calorias']
                }
            )
            
            if created:
                for refeicao_data in dieta_data['refeicoes']:
                    Refeicao.objects.create(
                        nome=refeicao_data['nome'],
                        descricao=refeicao_data['descricao'],
                        calorias=refeicao_data['calorias'],
                        dieta=dieta
                    )
    
    print(f"✅ Dietas criadas para {clientes.count()} clientes")

def create_historicos():
    print("📊 Criando históricos...")
    
    clientes = Cliente.objects.all()
    
    for cliente in clientes:
        treinos = Treino.objects.filter(cliente=cliente)
        dietas = Dieta.objects.filter(cliente=cliente)
        
        # Histórico de treinos
        for i, treino in enumerate(treinos[:2]):
            HistoricoTreino.objects.get_or_create(
                cliente=cliente,
                treino=treino,
                data_inicio=date.today() - timedelta(days=10 + i),
                defaults={
                    'data_fim': date.today() - timedelta(days=5 + i),
                    'observacoes': f'Treino executado com sucesso. Cliente demonstrou boa evolução.'
                }
            )
        
        # Histórico de dietas
        for i, dieta in enumerate(dietas[:1]):
            HistoricoDieta.objects.get_or_create(
                cliente=cliente,
                dieta=dieta,
                data_inicio=date.today() - timedelta(days=15),
                defaults={
                    'observacoes': 'Cliente seguiu a dieta conforme orientado.'
                }
            )
    
    print("✅ Históricos criados")

def create_trocas():
    print("🔄 Criando solicitações de troca...")
    
    clientes = Cliente.objects.all()[:2]  # Apenas os 2 primeiros clientes
    
    for cliente in clientes:
        treinos = Treino.objects.filter(cliente=cliente)
        dietas = Dieta.objects.filter(cliente=cliente)
        
        if treinos.exists():
            treino = treinos.first()
            exercicios = Exercicio.objects.filter(treino=treino)
            
            if exercicios.count() >= 2:
                TrocaExercicio.objects.get_or_create(
                    cliente=cliente,
                    exercicio_antigo=exercicios[0],
                    exercicio_novo=exercicios[1],
                    defaults={
                        'motivo': 'Exercício está causando desconforto no ombro',
                        'status': 'PENDENTE'
                    }
                )
        
        if dietas.exists():
            dieta = dietas.first()
            refeicoes = Refeicao.objects.filter(dieta=dieta)
            
            if refeicoes.count() >= 2:
                TrocaRefeicao.objects.get_or_create(
                    cliente=cliente,
                    refeicao_antiga=refeicoes[0],
                    refeicao_nova=refeicoes[1],
                    defaults={
                        'motivo': 'Alergia a um dos ingredientes',
                        'status': 'PENDENTE'
                    }
                )
    
    print("✅ Solicitações de troca criadas")

def main():
    print("🚀 Iniciando população do banco de dados...\n")
    
    try:
        create_users()
        create_tipo_planos()
        create_profiles()
        create_clientes()
        create_treinos()
        create_dietas()
        create_historicos()
        create_trocas()
        
        print("\n🎉 Banco de dados populado com sucesso!")
        print("\n📋 Resumo dos dados criados:")
        print(f"   👤 Usuários: {User.objects.count()}")
        print(f"   💳 Tipos de Plano: {TipoPlano.objects.count()}")
        print(f"   👥 Clientes: {Cliente.objects.count()}")
        print(f"   🏋️ Personal Trainers: {Personal.objects.count()}")
        print(f"   🥗 Nutricionistas: {Nutricionista.objects.count()}")
        print(f"   💪 Treinos: {Treino.objects.count()}")
        print(f"   🏃 Exercícios: {Exercicio.objects.count()}")
        print(f"   🥗 Dietas: {Dieta.objects.count()}")
        print(f"   🍽️ Refeições: {Refeicao.objects.count()}")
        print(f"   📊 Histórico Treinos: {HistoricoTreino.objects.count()}")
        print(f"   📊 Histórico Dietas: {HistoricoDieta.objects.count()}")
        print(f"   🔄 Trocas Exercícios: {TrocaExercicio.objects.count()}")
        print(f"   🔄 Trocas Refeições: {TrocaRefeicao.objects.count()}")
        
        print("\n🔑 Credenciais de acesso:")
        print("   Admin: admin / admin123")
        print("   Personal: carlos_personal / personal123")
        print("   Nutricionista: ana_nutri / nutri123")
        print("   Cliente: joao_cliente / cliente123")
        print("   Cliente: maria_cliente / cliente123")
        print("   Cliente: pedro_cliente / cliente123")
        print("   Cliente: ana_cliente / cliente123")
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()