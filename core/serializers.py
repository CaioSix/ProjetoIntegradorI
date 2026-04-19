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
    empresa = EmpresaSerializer(read_only=True)
    obrigacao = ObrigacaoSerializer(read_only=True)
    competencia = CompetenciaSerializer(read_only=True)

    empresa_id = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(),
        source='empresa',
        write_only=True
    )

    obrigacao_id = serializers.PrimaryKeyRelatedField(
        queryset=Obrigacao.objects.all(),
        source='obrigacao',
        write_only=True
    )

    competencia_id = serializers.PrimaryKeyRelatedField(
        queryset=Competencia.objects.all(),
        source='competencia',
        write_only=True
    )

    class Meta:
        model = Tarefa
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Tarefa.objects.all(),
                fields=['empresa', 'competencia', 'obrigacao']
            )
        ]

class TarefaDashboardSerializer(serializers.ModelSerializer):
    obrigacao_nome =serializers.CharField(source='obrigacao.nome')

    class Meta:
        model = Tarefa
        fields = ['id', 'obrigacao_nome', 'status', 'prazo']