from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from .models import (
    Empresa,
    Competencia,
    Obrigacao,
    Tarefa
)
from .serializers import (
    EmpresaSerializer,
    CompetenciaSerializer,
    ObrigacaoSerializer,
    TarefaSerializer,
    TarefaDashboardSerializer
)

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all().order_by('nome')
    serializer_class = EmpresaSerializer

class CompetenciaViewSet(viewsets.ModelViewSet):
    queryset = Competencia.objects.all()
    serializer_class = CompetenciaSerializer

class ObrigacaoViewSet(viewsets.ModelViewSet):
    queryset = Obrigacao.objects.all()
    serializer_class = ObrigacaoSerializer

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.select_related('empresa', 'obrigacao', 'competencia').order_by(F('prazo').asc(nulls_last=True))
    serializer_class = TarefaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'empresa', 'competencia', 'obrigacao']

@api_view(['GET'])
def dashboard_api(request):
    empresas = Empresa.objects.prefetch_related(
        Prefetch(
            'tarefas',
            queryset=Tarefa.objects.select_related(
                'obrigacao',
                'competencia'
            ).order_by(F('prazo').asc(nulls_last=True))
        )
    ).order_by('nome')

    resultado = []

    for empresa in empresas:
        tarefas = empresa.tarefas.all()

        resultado.append({
            "id": empresa.id,
            "nome": empresa.nome,
            "tipo": empresa.tipo,
            "pendentes": tarefas.filter(status='PENDENTE').count(),
            "concluidas": tarefas.filter(status='OK').count(),
            "tarefas": TarefaDashboardSerializer(tarefas, many=True).data
        })

    return Response({
        "empresas": resultado
    })