from .models import Tarefa, Competencia, Empresa, Obrigacao, TipoEmpresaObrigacao
from datetime import date, timedelta
import calendar

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

def gerar_competencia_atual():
    hoje = date.today()
    mes = hoje.month
    ano = hoje.year

    competencia, criada = Competencia.objects.get_or_create(
        mes=mes,
        ano=ano
    )

    if not criada:
        return competencia
        
    empresas = Empresa.objects.all()

    for empresa in empresas:
        relacoes = TipoEmpresaObrigacao.objects.filter(tipo_empresa=empresa.tipo)

        for rel in relacoes:
            obrigacao = rel.obrigacao

            prazo = None

            if obrigacao.dia_vencimento:
                ultimo_dia = calendar.monthrange(ano, mes)[1]
                dia = min(obrigacao.dia_vencimento, ultimo_dia)
                prazo = date(ano, mes, dia)

            Tarefa.objects.get_or_create(
                empresa=empresa,
                competencia=competencia,
                obrigacao=obrigacao,
                defaults={
                    "status": "PENDENTE",
                    "prazo": prazo
                }
            )

    return competencia
