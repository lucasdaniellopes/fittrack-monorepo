from django.contrib import admin
from .models import TipoPlano, Treino, Dieta, Cliente, HistoricoTreino, HistoricoDieta, Exercicio, Refeicao, TrocaExercicio, TrocaRefeicao

# Register your models here.
admin.site.register(TipoPlano)
admin.site.register(Treino)
admin.site.register(Dieta)
admin.site.register(Cliente)
admin.site.register(HistoricoTreino)
admin.site.register(HistoricoDieta)
admin.site.register(Exercicio)
admin.site.register(Refeicao)
admin.site.register(TrocaExercicio)
admin.site.register(TrocaRefeicao)
