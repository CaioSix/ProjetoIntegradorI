from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Empresa, Competencia, Obrigacao, Tarefa
from django.utils import timezone

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = '__all__'

class ObrigacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obrigacao
        fields = '__all__'

class TarefaSerializer(serializers.ModelSerializer):
    empresa_nome = serializers.CharField(source='empresa.nome')
    obrigacao_nome = serializers.CharField(source='obrigacao.nome')
    status_prazo = serializers.SerializerMethodField(method_name='calcular_prazo_status')
    prazo_formatado = serializers.SerializerMethodField(method_name='formata_prazo')

    class Meta:
        model = Tarefa
        fields = ['id', 'obrigacao_nome', 'status', 'status_prazo', 'prazo', 'prazo_formatado','empresa_nome']

    def calcular_prazo_status(self, obj):
        if not obj.prazo:
            return "Sem prazo"
        hoje = timezone.localdate()
        delta = (obj.prazo - hoje).days
        if delta < 0:
            return f"{abs(delta)} dias de atraso"
        elif delta == 0:
            return "Prazo é hoje"
        else:
            return f"{delta} dias para o prazo"
        
    def formata_prazo(self, obj):
        if not obj.prazo:
            return None
        return obj.prazo.strftime("%d/%m/%y")

class TarefaDashboardSerializer(serializers.ModelSerializer):
    obrigacao_nome =serializers.CharField(source='obrigacao.nome')

    class Meta:
        model = Tarefa
        fields = ['id', 'obrigacao_nome', 'status', 'prazo']