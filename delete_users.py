import os
import django

# Inicializa o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

def delete_all_appointments():
    User.objects.all().delete()

if __name__ == "__main__":
    delete_all_appointments()