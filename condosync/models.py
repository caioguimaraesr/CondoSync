from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.html import mark_safe

# Create your models here.
class Apartamento(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    morador = models.OneToOneField(User, on_delete=models.CASCADE, related_name="apartamento",null=True, blank=True)

    def __str__(self):
        if self.morador:
            return f"APTO{self.numero}: {self.morador.username}"
        return f"APTO{self.numero}"

class Boleto(models.Model):
    apartamentos = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    mes_referencia = models.CharField(max_length=26)
    arquivo = models.FileField(upload_to='documents/boletos/')

    def __str__(self):
        return f"{self.mes_referencia}: APTO{self.apartamentos.numero}"
    
class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Encomenda(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='encomendas')
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2) 
    origem = models.CharField(max_length=255)
    data_chegada = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Encomenda - APTO{self.apartamento.numero}"
    
class Veiculo(models.Model):
    TIPOS_DE_VEICULO = [
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
        ('Van', 'Van'),
        ('Outro', 'Outro')
    ]
    
    tipo_veiculo = models.CharField(max_length=50, choices=TIPOS_DE_VEICULO)
    placa = models.CharField(max_length=7, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    ano = models.CharField(max_length=4, default='0000')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='veiculos')

    def __str__(self):
        return f'{self.tipo_veiculo} - {self.modelo} {self.placa} - Proprietário: {self.usuario.username}'

class Ocorrencia(models.Model):
    titulo = models.CharField(max_length=100)
    desc = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ocorrencias')
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('resolvido', 'Resolvido')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Ocorrência: {self.titulo} - Morador: {self.usuario.username}"

class Sugestoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class VoceSabia(models.Model):
    titulo_1 = models.CharField(max_length=200)
    conteudo_1 = models.TextField()
    
    titulo_2 = models.CharField(max_length=200)
    conteudo_2 = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Você sabia? - Criado em {self.criado_em.strftime('%d/%m/%Y')}"
    
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Visitante(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='visitantes')
    data_visita = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - Apto {self.apartamento.numero}'

class AreaComum(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, help_text="Classe do ícone do BoxIcons, ex: 'bx bxs-party'")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    area = models.ForeignKey(AreaComum, on_delete=models.CASCADE, default=1)
    data = models.DateField()
    horario = models.TimeField()  # Agora é um TimeField simples, não mais uma ForeignKey

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('area', 'data', 'horario')
        ordering = ['-data', '-horario']

    def __str__(self):
        return f"{self.area.nome} - {self.usuario.get_full_name()} ({self.data}) {self.horario}"
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="Uma breve descrição sobre você")
    # foto_perfil = models.ImageField(upload_to='perfil/fotos/', blank=True, null=True)
    
    # Redes sociais (opcional)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    
    # Configurações de privacidade
    mostrar_telefone = models.BooleanField(default=True)
    mostrar_apartamento = models.BooleanField(default=True)
    
    @property
    def e_sindico(self):
        return self.usuario.is_superuser
    
    @property
    def apartamento(self):
        """Pega o apartamento vinculado ao User (do seu model Apartamento)"""
        return self.usuario.apartamento if hasattr(self.usuario, 'apartamento') else None
    
    def foto_perfil_html(self):
        """Exibe a foto do perfil no Admin (opcional)"""
        if self.foto_perfil:
            return mark_safe(f'<img src="{self.foto_perfil.url}" width="50px" />')
        return "Sem foto"
    foto_perfil_html.short_description = "Foto"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"