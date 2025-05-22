import os
import django
from datetime import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Horario

horarios = [
    (time(8, 0), time(10, 0)),
    (time(10, 0), time(12, 0)),
    (time(14, 0), time(16, 0)),
    (time(16, 0), time(18, 0)),
]

for inicio, fim in horarios:
    obj, created = Horario.objects.get_or_create(hora_inicio=inicio, hora_fim=fim)
    if created:
        print(f"Horário {inicio} - {fim} criado.")
    else:
        print(f"Horário {inicio} - {fim} já existe.")
