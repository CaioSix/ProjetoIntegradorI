from django.shortcuts import render
from .models import Empresa, Obrigacao, Tarefa, Competencia
from .utils import empresa_completa

def dashboard(request):
    competencia = Competencia.objects.order_by('-ano', '-mes').first()
    empresas = Empresa.objects.all()
    obrigacoes = Obrigacao.objects.all()

    tarefas = Tarefa.objects.filter(competencia=competencia)

    busca = request.GET.get('busca')
    status = request.GET.get('status')

    if busca:
        empresas = empresas.filter(nome__icontains=busca) | empresas.filter(codigo__icontains=busca)

    tabela = []

    for empresa in empresas:
        completa = empresa_completa(empresa, competencia)

        if status == 'completa' and not completa:
            continue
        if status == 'incompleta' and completa:
            continue
        
        linha = {
            "empresa": empresa,
            "completa": completa,
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

def lista_tarefas(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    tarefas = Tarefa.objects.filter(empresa=empresa)

    return render(request, 'core/tarefas.html', {
        'empresa': empresa,
        'tarefas': tarefas
    })