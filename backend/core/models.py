from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Perfil(BaseModel):
    ADMIN = 'admin'
    NUTRICIONISTA = 'nutricionista'
    PERSONAL = 'personal'
    CLIENTE = 'cliente'
    
    TIPO_CHOICES = [
        (ADMIN, 'Administrador'),
        (NUTRICIONISTA, 'Nutricionista'),
        (PERSONAL, 'Personal Trainer'),
        (CLIENTE, 'Cliente'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=CLIENTE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"

class TipoPlano(BaseModel):
    nome = models.CharField(max_length=100)  # ex: Mensal, Trimestral, Anual
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_dias = models.IntegerField()  # Duração em dias
    
    #para regras de negócio
    intervalo_atualizacao_treino_dieta = models.IntegerField(default=60, help_text="Intervalo em dias para atualização de treino e dieta")
    limite_trocas_exercicios = models.IntegerField(default=1, help_text="Número de trocas de exercícios permitidas")
    limite_trocas_refeicoes = models.IntegerField(default=1, help_text="Número de trocas de refeições permitidas")
    periodo_trocas_dias = models.IntegerField(default=7, help_text="Período em dias para realizar trocas após receber treino/dieta")
    trocas_ilimitadas = models.BooleanField(default=False, help_text="Se True, permite trocas ilimitadas de exercícios e refeições")

    def __str__(self):
        return self.nome

class Treino(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='treinos', null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome

class Dieta(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    calorias = models.IntegerField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='dietas', null=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.nome
    
class Cliente(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)  # em centímetros
    peso = models.FloatField(blank=True, null=True)    # em quilogramas
    tipo_plano = models.ForeignKey(TipoPlano, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes')
    data_inicio_plano = models.DateField(null=True, blank=True)
    data_fim_plano = models.DateField(null=True, blank=True)
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='cliente', null=True, blank=True)

    data_ultimo_treino = models.DateField(null=True, blank=True, help_text="Data em que o último treino foi atribuído")
    data_ultima_dieta = models.DateField(null=True, blank=True, help_text="Data em que a última dieta foi atribuída")
    trocas_exercicios_restantes = models.IntegerField(default=0, help_text="Número de trocas de exercícios restantes no período atual")
    trocas_refeicoes_restantes = models.IntegerField(default=0, help_text="Número de trocas de refeições restantes no período atual")
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Personal(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='personal', null=True, blank=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Personais"
    
    def __str__(self):
        return self.nome


class Nutricionista(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    crn = models.CharField(max_length=20, blank=True, null=True, help_text="Conselho Regional de Nutricionistas")
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='nutricionista', null=True, blank=True)
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class HistoricoTreino(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historico_treinos')
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.cliente.nome} - {self.treino.nome}"

class HistoricoDieta(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historico_dietas')
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.cliente.nome} - {self.dieta.nome} ({self.data_inicio})"



class Exercicio(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    
    def __str__(self):
        return f"{self.nome} ({self.treino.nome})"


class Refeicao(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    calorias = models.IntegerField()
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, related_name='refeicoes')
    
    def __str__(self):
        return f"{self.nome} ({self.dieta.nome})"


class TrocaExercicio(BaseModel):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='trocas_exercicios')
    exercicio_antigo = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='trocas_como_antigo')
    exercicio_novo = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='trocas_como_novo', null=True, blank=True)
    exercicio_sugerido = models.CharField(max_length=255, blank=True, null=True, help_text="Sugestão de exercício quando não há um específico")
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField(help_text="Motivo da solicitação de troca")
    observacoes_resposta = models.TextField(blank=True, null=True, help_text="Observações do profissional")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    aprovado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='exercicios_aprovados')
    
    class Meta:
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.exercicio_antigo.nome} ({self.status})"


class TrocaRefeicao(BaseModel):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='trocas_refeicoes')
    refeicao_antiga = models.ForeignKey(Refeicao, on_delete=models.CASCADE, related_name='trocas_como_antiga')
    refeicao_nova = models.ForeignKey(Refeicao, on_delete=models.CASCADE, related_name='trocas_como_nova', null=True, blank=True)
    refeicao_sugerida = models.CharField(max_length=255, blank=True, null=True, help_text="Sugestão de refeição quando não há uma específica")
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField(help_text="Motivo da solicitação de troca")
    observacoes_resposta = models.TextField(blank=True, null=True, help_text="Observações do profissional")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    aprovado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='refeicoes_aprovadas')
    
    class Meta:
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.refeicao_antiga.nome} ({self.status})"
