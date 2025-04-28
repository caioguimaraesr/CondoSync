from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
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