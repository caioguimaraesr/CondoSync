import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Boleto, Apartamento
from django.core.files import File

mes_referencia = 'Janeiro'
apartamento_101 = Apartamento.objects.get(numero=101)

novo_boleto = Boleto.objects.create(
    apartamentos=apartamento_101,
    mes_referencia=mes_referencia,
    arquivo='condosync/static/condosync/documentos/BOLETO_JANEIRO.pdf'
)