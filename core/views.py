from django.shortcuts import render
from datetime import date, timedelta
from .models import Empresa, Obrigacao, Tarefa, Competencia
from .utils import (
    empresa_completa,
    tarefas_normais,
    tarefas_proximas,
    tarefas_urgentes,
    gerar_competencia_atual
)
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

@login_required
def dashboard(request):
    competencia = gerar_competencia_atual()
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

@login_required
def lista_tarefas(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    tarefas = Tarefa.objects.filter(empresa=empresa)

    return render(request, 'core/tarefas.html', {
        'empresa': empresa,
        'tarefas': tarefas
    })

@login_required
def todas_tarefas(request):
    filtro = request.GET.get('filtro')

    tarefas = []

    for t in tarefas_urgentes().select_related('empresa', 'obrigacao').order_by('prazo'):
        tarefas.append({
            'tarefa': t,
            'prioridade': 'urgente'
        })

    for t in tarefas_proximas().select_related('empresa', 'obrigacao').order_by('prazo'):
        tarefas.append({
            'tarefa': t,
            'prioridade': 'proxima'
        })

    if not filtro:
        for t in tarefas_normais().select_related('empresa', 'obrigacao').order_by('prazo'):
            tarefas.append({
                'tarefa': t,
                'prioridade': 'normal'
            })

    if filtro == 'urgentes':
        tarefas = [t for t in tarefas if t['prioridade'] == 'urgente']

    elif filtro == 'proximas':
        tarefas = [t for t in tarefas if t['prioridade'] == 'proxima']

    return render(request, 'core/todas_tarefas.html', {
        'tarefas': tarefas,
        'filtro': filtro
    })