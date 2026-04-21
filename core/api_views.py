from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Case, When, IntegerField, Value
from datetime import date, timedelta
from django.utils import timezone
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

    @action(detail=True, methods=['patch'])
    def concluir(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.status == 'CONCLUIDA':
            return Response(
                {"erro": "Tarefa já está concluída"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tarefa.status == 'DISPENSADA':
            return Response(
                {"erro": "Tarefa dispensada não pode ser reaberta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'CONCLUIDA'
        tarefa.concluida_em = timezone.localdate()
        tarefa.save()

        return Response({
            "mensagem": "Tarefa concluída com sucesso",
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
        })
    
    @action(detail=True, methods=['patch'])
    def reabrir(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.status == 'PENDENTE':
            return Response(
                {"erro": "Tarefa já está pendente"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tarefa.status == 'DISPENSADA':
            return Response(
                {"erro": "Tarefa dispensada não pode ser reaberta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'PENDENTE'
        tarefa.concluida_em = None
        tarefa.save()

        return Response({
            "mensagem": "Tarefa reaberta com sucesso",
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
        })
    
    @action(detail=True, methods=['patch'])
    def dispensar(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.status == 'DISPENSADA':
            return Response(
                {"erro": "Tarefa já está dispensada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'DISPENSADA'
        tarefa.concluida_em = None
        tarefa.save()

        return Response({
            "mensagem": "Tarefa dispensada com sucesso",
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
        })

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
            "concluidas": tarefas.filter(status='CONCLUIDA').count(),
            "tarefas": TarefaDashboardSerializer(tarefas, many=True).data
        })

    return Response({
        "empresas": resultado
    })

@api_view(['GET'])
def tarefas_geral(request):
    hoje = date.today()
    limite = hoje + timedelta(days=7)

    tarefas = Tarefa.objects.select_related('empresa', 'obrigacao', 'competencia').filter(status='PENDENTE')

    tarefas = tarefas.annotate(
        prioridade=Case(
            When(prazo__lt=hoje, then=Value(1)),
            When(prazo=hoje, then=Value(2)),
            When(prazo__lte=limite, then=Value(3)),
            When(prazo__isnull=True, then=Value(5)),
            default=Value(4),
            output_field=IntegerField()
        )
    ).order_by('prioridade', 'prazo')

    return Response({
        "tarefas": TarefaSerializer(tarefas, many=True).data
    })