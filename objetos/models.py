from django.db import models

class Material (models.Model):
    cm = models.CharField(max_length=8)
    retranca = models.CharField(max_length=100)
    duracao = models.IntegerField()
    tipo = models.CharField(max_length=2)
    cliente = models.CharField(max_length=100)
    choques = models.CharField(max_length=100)
    exibicao = models.CharField(max_length=1)
    data = models.CharField(max_length=10)
    pt = models.CharField(max_length=5)
    programa = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.retranca} ({self.programa}, {self.pt})"