import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import AreaComum

areas = [
    ('Salão de Festas', 'bx bxs-party'),
]

for nome, icone in areas:
    area, created = AreaComum.objects.get_or_create(nome=nome, icone=icone)
    if created:
        print(f"Área comum '{nome}' criada.")
    else:
        print(f"Área comum '{nome}' já existe.")
