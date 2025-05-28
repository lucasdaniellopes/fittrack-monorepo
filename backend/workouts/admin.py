from django.contrib import admin
from .models import Treino, Exercicio, HistoricoTreino, TrocaExercicio

admin.site.register(Treino)
admin.site.register(Exercicio)
admin.site.register(HistoricoTreino)
admin.site.register(TrocaExercicio)