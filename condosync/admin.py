from django.contrib import admin
from .models import Boleto, Apartamento, Aviso, Encomenda, Veiculo, Ocorrencia, Sugestoes, VoceSabia
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