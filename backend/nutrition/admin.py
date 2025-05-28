from django.contrib import admin
from .models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao

admin.site.register(Dieta)
admin.site.register(Refeicao)
admin.site.register(HistoricoDieta)
admin.site.register(TrocaRefeicao)