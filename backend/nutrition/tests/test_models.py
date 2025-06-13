from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao


class DietaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
    
    def test_dieta_creation(self):
        dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        self.assertEqual(dieta.nome, "Dieta Teste")
        self.assertEqual(dieta.calorias, 2000)
        self.assertEqual(dieta.cliente, self.cliente)
        self.assertIsNotNone(dieta.created_at)
    
    def test_dieta_str_representation(self):
        dieta = Dieta.objects.create(
            nome="Dieta Low Carb",
            descricao="Dieta com baixo carboidrato",
            calorias=1800,
            cliente=self.cliente
        )
        self.assertEqual(str(dieta), "Dieta Low Carb")
    
    def test_dieta_without_cliente(self):
        dieta = Dieta.objects.create(
            nome="Dieta Genérica",
            descricao="Dieta sem cliente específico",
            calorias=2200
        )
        self.assertIsNone(dieta.cliente)
        self.assertEqual(dieta.nome, "Dieta Genérica")
    
    def test_dieta_ordering(self):
        dieta1 = Dieta.objects.create(
            nome="Dieta 1",
            descricao="Primeira dieta",
            calorias=2000,
            cliente=self.cliente
        )
        dieta2 = Dieta.objects.create(
            nome="Dieta 2",
            descricao="Segunda dieta",
            calorias=1800,
            cliente=self.cliente
        )
        
        dietas = list(Dieta.objects.all())
        # Deve estar ordenado por -created_at (mais recente primeiro)
        self.assertEqual(dietas[0], dieta2)
        self.assertEqual(dietas[1], dieta1)


class RefeicaoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
    
    def test_refeicao_creation(self):
        refeicao = Refeicao.objects.create(
            nome="Café da Manhã",
            descricao="Primeira refeição do dia",
            calorias=300,
            dieta=self.dieta
        )
        self.assertEqual(refeicao.nome, "Café da Manhã")
        self.assertEqual(refeicao.calorias, 300)
        self.assertEqual(refeicao.dieta, self.dieta)
        self.assertIsNotNone(refeicao.created_at)
    
    def test_refeicao_str_representation(self):
        refeicao = Refeicao.objects.create(
            nome="Almoço",
            descricao="Refeição principal",
            calorias=600,
            dieta=self.dieta
        )
        expected = f"Almoço ({self.dieta.nome})"
        self.assertEqual(str(refeicao), expected)
    
    def test_multiple_refeicoes_per_dieta(self):
        cafe = Refeicao.objects.create(
            nome="Café da Manhã",
            descricao="Primeira refeição",
            calorias=300,
            dieta=self.dieta
        )
        almoco = Refeicao.objects.create(
            nome="Almoço",
            descricao="Segunda refeição",
            calorias=600,
            dieta=self.dieta
        )
        
        refeicoes_da_dieta = Refeicao.objects.filter(dieta=self.dieta)
        self.assertEqual(refeicoes_da_dieta.count(), 2)
        self.assertIn(cafe, refeicoes_da_dieta)
        self.assertIn(almoco, refeicoes_da_dieta)
    
    def test_refeicao_ordering(self):
        # Criar refeições fora de ordem alfabética
        jantar = Refeicao.objects.create(
            nome="Jantar",
            descricao="Última refeição",
            calorias=500,
            dieta=self.dieta
        )
        almoco = Refeicao.objects.create(
            nome="Almoço",
            descricao="Refeição do meio-dia",
            calorias=600,
            dieta=self.dieta
        )
        
        refeicoes = list(Refeicao.objects.filter(dieta=self.dieta))
        # Deve estar ordenado por nome
        self.assertEqual(refeicoes[0], almoco)  # "Almoço" vem antes
        self.assertEqual(refeicoes[1], jantar)  # "Jantar" vem depois


class HistoricoDietaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
    
    def test_historico_dieta_creation(self):
        historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15",
            observacoes="Dieta iniciada com sucesso"
        )
        self.assertEqual(historico.cliente, self.cliente)
        self.assertEqual(historico.dieta, self.dieta)
        self.assertEqual(str(historico.data_inicio), "2024-01-15")
        self.assertEqual(historico.observacoes, "Dieta iniciada com sucesso")
    
    def test_historico_dieta_str_representation(self):
        historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15"
        )
        expected = f"{self.cliente.nome} - {self.dieta.nome} (2024-01-15)"
        self.assertEqual(str(historico), expected)
    
    def test_historico_dieta_with_data_fim(self):
        historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15",
            data_fim="2024-01-30"
        )
        self.assertEqual(str(historico.data_inicio), "2024-01-15")
        self.assertEqual(str(historico.data_fim), "2024-01-30")
    
    def test_historico_dieta_without_observacoes(self):
        historico = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15"
        )
        self.assertIsNone(historico.observacoes)
    
    def test_multiple_historicos_per_cliente(self):
        historico1 = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=self.dieta,
            data_inicio="2024-01-15"
        )
        
        dieta2 = Dieta.objects.create(
            nome="Dieta 2",
            descricao="Segunda dieta",
            calorias=1800,
            cliente=self.cliente
        )
        
        historico2 = HistoricoDieta.objects.create(
            cliente=self.cliente,
            dieta=dieta2,
            data_inicio="2024-01-20"
        )
        
        historicos_do_cliente = HistoricoDieta.objects.filter(cliente=self.cliente)
        self.assertEqual(historicos_do_cliente.count(), 2)


class TrocaRefeicaoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.perfil = Perfil.objects.get(usuario=self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            email="cliente@test.com",
            perfil=self.perfil
        )
        
        self.dieta = Dieta.objects.create(
            nome="Dieta Teste",
            descricao="Descrição da dieta",
            calorias=2000,
            cliente=self.cliente
        )
        
        self.refeicao_antiga = Refeicao.objects.create(
            nome="Café da Manhã Original",
            descricao="Refeição original",
            calorias=300,
            dieta=self.dieta
        )
        
        self.refeicao_nova = Refeicao.objects.create(
            nome="Café da Manhã Alternativo",
            descricao="Refeição alternativa",
            calorias=320,
            dieta=self.dieta
        )
    
    def test_troca_refeicao_creation(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Intolerância alimentar"
        )
        self.assertEqual(troca.cliente, self.cliente)
        self.assertEqual(troca.refeicao_antiga, self.refeicao_antiga)
        self.assertEqual(troca.refeicao_nova, self.refeicao_nova)
        self.assertEqual(troca.motivo, "Intolerância alimentar")
        self.assertEqual(troca.status, 'PENDENTE')  # Status padrão
    
    def test_troca_refeicao_str_representation(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Preferência pessoal"
        )
        expected = f"{self.cliente.nome} - {self.refeicao_antiga.nome} (PENDENTE)"
        self.assertEqual(str(troca), expected)
    
    def test_troca_refeicao_status_choices(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Teste"
        )
        
        # Testar diferentes status
        troca.status = 'APROVADO'
        troca.save()
        self.assertEqual(troca.status, 'APROVADO')
        
        troca.status = 'REJEITADO'
        troca.save()
        self.assertEqual(troca.status, 'REJEITADO')
    
    def test_troca_refeicao_with_sugestao(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_sugerida="Aveia com frutas",
            motivo="Quero algo mais leve"
        )
        self.assertEqual(troca.refeicao_sugerida, "Aveia com frutas")
        self.assertIsNone(troca.refeicao_nova)
    
    def test_troca_refeicao_approval_fields(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Teste",
            status='APROVADO',
            aprovado_por=self.admin_user,
            observacoes_resposta="Aprovado pela nutricionista"
        )
        self.assertEqual(troca.aprovado_por, self.admin_user)
        self.assertEqual(troca.observacoes_resposta, "Aprovado pela nutricionista")
    
    def test_troca_refeicao_data_solicitacao_auto(self):
        troca = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Teste"
        )
        # Verificar se data_solicitacao foi definida automaticamente
        self.assertIsNotNone(troca.data_solicitacao)
    
    def test_troca_refeicao_ordering(self):
        troca1 = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_antiga,
            refeicao_nova=self.refeicao_nova,
            motivo="Primeira troca"
        )
        
        troca2 = TrocaRefeicao.objects.create(
            cliente=self.cliente,
            refeicao_antiga=self.refeicao_nova,
            refeicao_sugerida="Outra opção",
            motivo="Segunda troca"
        )
        
        trocas = list(TrocaRefeicao.objects.all())
        # Deve estar ordenado por -data_solicitacao (mais recente primeiro)
        self.assertEqual(trocas[0], troca2)
        self.assertEqual(trocas[1], troca1)