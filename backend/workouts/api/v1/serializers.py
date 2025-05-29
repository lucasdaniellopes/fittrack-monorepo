from rest_framework import serializers
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio

class TreinoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Treino
        fields = ['id', 'nome', 'descricao', 'duracao', 'cliente', 'cliente_nome', 'created_at', 'updated_at']

class ExercicioSerializer(serializers.ModelSerializer):
    treino_nome = serializers.CharField(source='treino.nome', read_only=True)
    
    class Meta:
        model = Exercicio
        fields = ['id', 'nome', 'descricao', 'treino', 'treino_nome', 'created_at', 'updated_at']

class HistoricoTreinoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    treino_nome = serializers.CharField(source='treino.nome', read_only=True)
    
    class Meta:
        model = HistoricoTreino
        fields = ['id', 'cliente', 'cliente_nome', 'treino', 'treino_nome', 'data_inicio', 'data_fim', 'observacoes', 'created_at', 'updated_at']

class TrocaExercicioSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    exercicio_antigo_nome = serializers.CharField(source='exercicio_antigo.nome', read_only=True)
    exercicio_novo_nome = serializers.CharField(source='exercicio_novo.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrocaExercicio
        fields = '__all__'