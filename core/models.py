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
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizada_em = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    def __str__(self):
        return f"{self.nome} ({self.codigo})"
    
class Competencia(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    class Meta:
        unique_together = ('mes', 'ano')
        ordering = ['-ano', '-mes']

    def __str__(self):
        return f"{self.mes}/{self.ano}"
    
class Obrigacao(models.Model):
    nome = models.CharField(max_length=100)
    dia_vencimento = models.IntegerField(null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizada_em = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    STATUS_CHOICE = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDA', 'Concluída'),
        ('DISPENSADA', 'Dispensada')
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tarefas')
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, related_name='tarefas')
    obrigacao = models.ForeignKey(Obrigacao, on_delete=models.CASCADE, related_name='tarefas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='PENDENTE')
    prazo = models.DateField(null=True, blank=True)
    concluida_em = models.DateField(null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizada_em = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    class Meta:
        unique_together = ('empresa', 'competencia', 'obrigacao')

    def __str__(self):
        return f"{self.empresa} - {self.obrigacao} - {self.competencia} - {self.status} - {self.prazo}"
    
class TipoEmpresaObrigacao(models.Model):
    tipo_empresa = models.CharField(max_length=20, choices=Empresa.TIPO_CHOICES)
    obrigacao = models.ForeignKey(Obrigacao, on_delete=models.CASCADE, related_name='tipos_empresa')
    criada_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    class Meta:
        unique_together = ('tipo_empresa', 'obrigacao')

        def __str__(self):
            return f"{self.tipo_empresa} - {self.obrigacao.nome}"