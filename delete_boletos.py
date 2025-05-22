import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Boleto

def delete_all_appointments():
    Boleto.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()