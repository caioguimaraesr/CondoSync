from django.contrib import admin
from .models import Boleto, Apartamento, Aviso, Encomenda, Veiculo, Ocorrencia, Sugestoes, VoceSabia, Funcionario, Visitante, AreaComum, Horario, Reserva, Perfil
# Register your models here.

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    ...

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    ...

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    ...

@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    ...

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    ...

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    ...

@admin.register(Sugestoes)
class SugestoesAdmin(admin.ModelAdmin):
    ...

@admin.register(VoceSabia)
class VoceSabiaAdmin(admin.ModelAdmin):
    ...

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    ...

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    ...

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    ...

@admin.register(AreaComum)
class AreaComumAdmin(admin.ModelAdmin):
    ...

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    ...

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    ...