import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import Sugestoes

def delete_all_appointments():
    Sugestoes.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()