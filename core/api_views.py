from rest_framework import viewsets
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
    TarefaSerializer
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
    filterser_fields = ['status', 'empresa', 'competencia', 'obrigacao']