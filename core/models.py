from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    
class Competencia(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.mes}/{self.ano}"
    
class Obrigacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    STATUS_CHOICE = [
        ('PENDENTE', 'Pendente'),
        ('OK', 'ok'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    obrigacao = models.ForeignKey(Obrigacao, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='PENDENTE')

    def __str__(self):
        return f"{self.empresa} - {self.obrigacao} - {self.competencia}"