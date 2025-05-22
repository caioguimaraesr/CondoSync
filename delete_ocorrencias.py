import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Ocorrencia

def delete_all_appointments():
    Ocorrencia.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()