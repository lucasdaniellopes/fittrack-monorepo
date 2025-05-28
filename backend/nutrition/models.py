from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from accounts.models import Cliente


class Dieta(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    calorias = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='dietas', null=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.nome


class Refeicao(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    calorias = models.IntegerField()
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, related_name='refeicoes')
    
    def __str__(self):
        return f"{self.nome} ({self.dieta.nome})"


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