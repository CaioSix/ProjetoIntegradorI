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
    class Meta:
        model = Tarefa
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Tarefa.objects.all(),
                fields=['empresa', 'competencia', 'obrigacao']
            )
        ]