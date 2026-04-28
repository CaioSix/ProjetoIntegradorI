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
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    obrigacao_nome = serializers.CharField(source='obrigacao.nome', read_only=True)
    empresa_id = serializers.IntegerField(source='empresa.id', read_only=True)
    obrigacao_id = serializers.IntegerField(source='obrigacao.id', read_only=True)
    status_prazo = serializers.SerializerMethodField(method_name='calcular_prazo_status', read_only=True)
    prazo_formatado = serializers.SerializerMethodField(method_name='formata_prazo', read_only=True)
    dias_prazo = serializers.SerializerMethodField(method_name='dias_para_prazo')
    prioridade = serializers.IntegerField(read_only=True, default=4)

    class Meta:
        model = Tarefa
        fields = ['id', 'empresa_id', 'empresa_nome', 'obrigacao_nome', 'obrigacao_id', 'obrigacao_nome','status', 'status_prazo', 'prazo', 'prazo_formatado', 'dias_prazo', 'prioridade']
        read_only_fields = ['status', 'concluida_em']

    def calcular_prazo_status(self, obj):
        if not obj.prazo:
            return "Sem prazo"
        hoje = timezone.localdate()
        dias = (obj.prazo - hoje).days
        if dias < 0:
            return f"{abs(dias)} dias de atraso"
        elif dias == 0:
            return "Prazo é hoje"
        else:
            return f"{dias} dias para o prazo"
        
    def formata_prazo(self, obj):
        if not obj.prazo:
            return None
        return obj.prazo.strftime("%d/%m/%Y")
    
    def dias_para_prazo(self, obj):
        if not obj.prazo:
            return None
        
        hoje = timezone.localdate()
        return (obj.prazo - hoje).days

class TarefaDashboardSerializer(serializers.ModelSerializer):
    obrigacao_nome =serializers.CharField(source='obrigacao.nome')
    obrigacao_id = serializers.IntegerField(source='obrigacao_id')
    empresa_id = serializers.IntegerField(source='empresa_id')
    

    class Meta:
        model = Tarefa
        fields = ['id','empresa_id', 'obrigacao_id', 'obrigacao_nome', 'status', 'prazo']