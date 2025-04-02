from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Apartamento(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    morador = models.OneToOneField(User, on_delete=models.CASCADE, related_name="apartamento")

    def __str__(self):
        return f"APTO{self.numero}: {self.morador.username}"

class Boleto(models.Model):
    apartamentos = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    mes_referencia = models.CharField(max_length=26)
    arquivo = models.FileField(upload_to='documents/boletos/')

    def __str__(self):
        return f"{self.mes_referencia}: APTO{self.apartamentos.numero}"