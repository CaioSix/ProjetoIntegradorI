from django.shortcuts import render
from .models import Empresa, Obrigacao, Tarefa, Competencia

def dashboard(request):
    competencia = Competencia.objects.first()
    empresas = Empresa.objects.all()
    obrigacoes = Obrigacao.objects.all()

    tarefas = Tarefa.objects.filter(competencia=competencia)

    tabela = []

    for empresa in empresas:
        linha = {
            "empresa": empresa,
            "tarefas": []
        }

        for obrigacao in obrigacoes:
            tarefa = tarefas.filter(
                empresa=empresa,
                obrigacao=obrigacao
            ).first()

            linha["tarefas"].append(tarefa)

        tabela.append(linha)

    return render(request, 'core/dashboard.html', {
        'tabela': tabela,
        'obrigacoes': obrigacoes,
        'competencias': competencia
    })