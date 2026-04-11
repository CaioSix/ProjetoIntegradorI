from django.db import models

class Empresa(models.Model):
    TIPO_CHOICES = [
        ('SN_COM_FOLHA', 'Simples Nacional com Folha'),
        ('SN_SEM_FOLHA', 'Simples Nacional sem Folha'),
        ('MEI', 'MEI'),
        ('LUCRO_PRESUMIDO', 'Lucro Presumido'),
    ]

    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, unique=True, db_index=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return F"{self.nome} ({self.codigo})"
    
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
    prazo = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.empresa} - {self.obrigacao} - {self.competencia}"