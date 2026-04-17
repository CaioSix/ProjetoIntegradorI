from rest_framework import viewsets
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
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class CompetenciaViewSet(viewsets.ModelViewSet):
    queryset = Competencia.objects.all()
    serializer_class = CompetenciaSerializer

class ObrigacaoViewSet(viewsets.ModelViewSet):
    queryset = Obrigacao.objects.all()
    serializer_class = ObrigacaoSerializer

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer