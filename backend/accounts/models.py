from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


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
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_dias = models.IntegerField()
    
    intervalo_atualizacao_treino_dieta = models.IntegerField(default=60, help_text="Intervalo em dias para atualização de treino e dieta")
    limite_trocas_exercicios = models.IntegerField(default=1, help_text="Número de trocas de exercícios permitidas")
    limite_trocas_refeicoes = models.IntegerField(default=1, help_text="Número de trocas de refeições permitidas")
    periodo_trocas_dias = models.IntegerField(default=7, help_text="Período em dias para realizar trocas após receber treino/dieta")
    trocas_ilimitadas = models.BooleanField(default=False, help_text="Se True, permite trocas ilimitadas de exercícios e refeições")

    def __str__(self):
        return self.nome


class Cliente(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
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