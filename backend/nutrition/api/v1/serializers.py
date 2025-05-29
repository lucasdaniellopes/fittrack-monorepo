from rest_framework import serializers
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao

class DietaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Dieta
        fields = ['id', 'nome', 'descricao', 'calorias', 'cliente', 'cliente_nome', 'created_at', 'updated_at']

class RefeicaoSerializer(serializers.ModelSerializer):
    dieta_nome = serializers.CharField(source='dieta.nome', read_only=True)
    
    class Meta:
        model = Refeicao
        fields = ['id', 'nome', 'descricao', 'calorias', 'dieta', 'dieta_nome', 'created_at', 'updated_at']

class HistoricoDietaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    dieta_nome = serializers.CharField(source='dieta.nome', read_only=True)
    
    class Meta:
        model = HistoricoDieta
        fields = ['id', 'cliente', 'cliente_nome', 'dieta', 'dieta_nome', 'data_inicio', 'data_fim', 'observacoes', 'created_at', 'updated_at']

class TrocaRefeicaoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    refeicao_antiga_nome = serializers.CharField(source='refeicao_antiga.nome', read_only=True)
    refeicao_nova_nome = serializers.CharField(source='refeicao_nova.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrocaRefeicao
        fields = '__all__'