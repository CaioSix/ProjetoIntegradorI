from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Empresa, Competencia, Obrigacao, Tarefa

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

    class Meta:
        model = Tarefa
        fields = ['id', 'obrigacao_nome', 'status', 'prazo', 'empresa_nome']

class TarefaDashboardSerializer(serializers.ModelSerializer):
    obrigacao_nome =serializers.CharField(source='obrigacao.nome')

    class Meta:
        model = Tarefa
        fields = ['id', 'obrigacao_nome', 'status', 'prazo']