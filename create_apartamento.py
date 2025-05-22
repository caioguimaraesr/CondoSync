import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Apartamento

numeros = ['101', '102', '103', '104']

for numero in numeros:
    apt, created = Apartamento.objects.get_or_create(numero=numero)
    if created:
        print(f"Apartamento {numero} criado.")
    else:
        print(f"Apartamento {numero} já existe.")   