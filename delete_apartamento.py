import os
import django

# Inicializa o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Apartamento

def delete_all_appointments():
    Apartamento.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()