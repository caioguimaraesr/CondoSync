import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from condosync.models import VoceSabia

titulo_1 = 'Titulo 1 criado para teste'
conteudo_1 = 'Conteudo 1 criado para teste'

titulo_2 = 'Titulo 2 criado para teste'
conteudo_2 = 'Conteudo 2 criado para teste'

novo_objeto = VoceSabia.objects.create(
   titulo_1=titulo_1,
   conteudo_1=conteudo_1,
   titulo_2=titulo_2,
   conteudo_2=conteudo_2,
)
