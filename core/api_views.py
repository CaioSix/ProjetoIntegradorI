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
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView

class LoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return super().post(request, format=None)

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
    def concluir(self, request, pk=None, pagination_class=None):
        tarefa = self.get_object()

        if tarefa.status == 'CONCLUIDA':
            return Response(
                {"message": "Tarefa já está concluída"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tarefa.status == 'DISPENSADA':
            return Response(
                {"message": "Tarefa dispensada não pode ser reaberta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'CONCLUIDA'
        tarefa.concluida_em = timezone.localdate()
        tarefa.save()

        return Response({
            "mensagem": "Tarefa concluída com sucesso",
            "data": {
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
            }
        })
    
    @action(detail=True, methods=['patch'], pagination_class=None)
    def reabrir(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.status == 'PENDENTE':
            return Response(
                {"message": "Tarefa já está pendente"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if tarefa.status == 'DISPENSADA':
            return Response(
                {"message": "Tarefa dispensada não pode ser reaberta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'PENDENTE'
        tarefa.concluida_em = None
        tarefa.save()

        return Response({
            "mensagem": "Tarefa reaberta com sucesso",
            "data": {
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
            }
        })
    
    @action(detail=True, methods=['patch'], pagination_class=None)
    def dispensar(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.status == 'DISPENSADA':
            return Response(
                {"message": "Tarefa já está dispensada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tarefa.status = 'DISPENSADA'
        tarefa.concluida_em = None
        tarefa.save()

        return Response({
            "mensagem": "Tarefa dispensada com sucesso",
            "data": {
            "id": tarefa.id,
            "status": tarefa.status,
            "concluida_em": tarefa.concluida_em
            }
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
            "empresa_id": empresa.id,
            "empresa_nome": empresa.nome,
            "tipo": empresa.tipo,
            "pendentes": tarefas.filter(status='PENDENTE').count(),
            "concluidas": tarefas.filter(status='CONCLUIDA').count(),
            "tarefas": TarefaDashboardSerializer(tarefas, many=True).data
        })

    return Response({
        "results": resultado
    })

@api_view(['GET'])
def tarefas_pendentes(request):
    hoje = timezone.localdate()
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

    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginator.page_size_query_param = 'page_size'
    page = paginator.paginate_queryset(tarefas, request)
    serializer = TarefaSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)