from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from accounts.models import Cliente


class Treino(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='treinos', null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome


class Exercicio(BaseModel):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    
    def __str__(self):
        return f"{self.nome} ({self.treino.nome})"


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