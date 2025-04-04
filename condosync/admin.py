from django.contrib import admin
from .models import Boleto, Apartamento, Aviso, Encomenda
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