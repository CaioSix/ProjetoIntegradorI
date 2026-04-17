from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import calendar
from .models import (
    Empresa,
    Competencia,
    Tarefa,
    TipoEmpresaObrigacao
)

@receiver(post_save, sender=Empresa)
def criar_tarefas_para_nova_empresa(sender, instance, created, **kwargs):
    if not created:
        return
    
    hoje = date.today()
    mes = hoje.month
    ano = hoje.year
    competencia, _ = Competencia.objects.get_or_create(
        mes=mes,
        ano=ano
    )
    relacoes = TipoEmpresaObrigacao.objects.filter(tipo_empresa=instance.tipo)

    for rel in relacoes:
        obrigacao = rel.obrigacao
        prazo = None
        if obrigacao.dia_vencimento:
            ultimo_dia = calendar.monthrange(ano, mes)[1]
            dia = min(obrigacao.dia_vencimento, ultimo_dia)
            prazo = date(ano, mes, dia)

        Tarefa.objects.get_or_create(
            empresa=instance,
            competencia=competencia,
            obrigacao=obrigacao,
            defaults={
                "status": "PENDENTE",
                "prazo": prazo
            }
        )