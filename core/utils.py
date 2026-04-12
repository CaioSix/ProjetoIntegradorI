from .models import Tarefa
from datetime import date, timedelta

def empresa_completa(empresa, competencia):
    tarefas = Tarefa.objects.filter(empresa=empresa, competencia=competencia)
    return tarefas.exists() and not tarefas.filter(status='PENDENTE').exists()

def tarefas_proximas():
    hoje = date.today()
    inicio_proximas = hoje + timedelta(days=7)
    fim_proximas = hoje + timedelta(days=1)

    return Tarefa.objects.filter(
        status='PENDENTE',
        prazo__gte=fim_proximas,
        prazo__lte=inicio_proximas
    )

def tarefas_urgentes():
    hoje = date.today()
    return Tarefa.objects.filter(status='PENDENTE', prazo__lte=hoje)

def tarefas_normais():
    hoje = date.today()
    limite = hoje + timedelta(days=7)

    return Tarefa.objects.filter(
        status='PENDENTE',
        prazo__gt=limite
    )