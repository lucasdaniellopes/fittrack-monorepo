from django.contrib import admin
from .models import Perfil, TipoPlano, Cliente, Personal, Nutricionista

admin.site.register(Perfil)
admin.site.register(TipoPlano)
admin.site.register(Cliente)
admin.site.register(Personal)
admin.site.register(Nutricionista)