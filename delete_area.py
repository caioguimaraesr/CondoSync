import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import AreaComum

def delete_all_appointments():
    AreaComum.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()