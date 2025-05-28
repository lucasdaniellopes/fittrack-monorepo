from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Perfil, TipoPlano, Cliente
from workouts.models import Treino, Exercicio, HistoricoTreino, TrocaExercicio
from nutrition.models import Dieta, Refeicao, HistoricoDieta, TrocaRefeicao

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    perfil = serializers.SerializerMethodField(read_only=True)
    tipo_perfil = serializers.CharField(write_only=True, required=False, help_text="Tipo do perfil: cliente, personal, nutricionista ou admin")
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 
                 'is_active', 'date_joined', 'password', 'perfil', 'tipo_perfil']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, attrs):
        # Require password for creation
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({"password": "This field is required for user creation."})
        
        # Validate tipo_perfil if provided
        tipo_perfil = attrs.get('tipo_perfil')
        if tipo_perfil and tipo_perfil not in ['admin', 'cliente', 'personal', 'nutricionista']:
            raise serializers.ValidationError({"tipo_perfil": "Invalid tipo_perfil. Must be one of: admin, cliente, personal, nutricionista"})
        
        return attrs
    
    def get_perfil(self, obj):
        if hasattr(obj, 'perfil'):
            return {
                'id': obj.perfil.id,
                'tipo': obj.perfil.tipo,
                'telefone': obj.perfil.telefone,
                'data_nascimento': obj.perfil.data_nascimento
            }
        return None
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        tipo_perfil = validated_data.pop('tipo_perfil', 'cliente')  # Remove tipo_perfil do validated_data
        
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # This should not happen due to validation, but as a fallback
            user.set_unusable_password()
        user.save()
        
        # Atualiza o tipo do perfil se foi especificado
        if hasattr(user, 'perfil') and tipo_perfil:
            user.perfil.tipo = tipo_perfil
            user.perfil.save()
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class PerfilSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    usuario_details = UserSerializer(source='usuario', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'usuario_details', 'tipo', 'tipo_display', 'telefone', 'data_nascimento']

class TreinoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Treino
        fields = ['id', 'nome', 'descricao', 'duracao', 'cliente', 'cliente_nome', 'created_at', 'updated_at']

class DietaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Dieta
        fields = ['id', 'nome', 'descricao', 'calorias', 'cliente', 'cliente_nome', 'created_at', 'updated_at']

class TipoPlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPlano
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    tipo_plano_nome = serializers.CharField(source='tipo_plano.nome', read_only=True)
    perfil = PerfilSerializer(read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'telefone', 'data_nascimento', 'altura', 'peso', 
                 'tipo_plano', 'tipo_plano_nome', 'data_inicio_plano', 'data_fim_plano',
                 'data_ultimo_treino', 'data_ultima_dieta',
                 'trocas_exercicios_restantes', 'trocas_refeicoes_restantes', 'perfil']

class HistoricoTreinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoTreino
        fields = '__all__'

class HistoricoDietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoDieta
        fields = '__all__'

class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercicio
        fields = '__all__'

class RefeicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refeicao
        fields = '__all__'

class TrocaExercicioSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    exercicio_antigo_nome = serializers.CharField(source='exercicio_antigo.nome', read_only=True)
    exercicio_novo_nome = serializers.CharField(source='exercicio_novo.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrocaExercicio
        fields = '__all__'

class TrocaRefeicaoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    refeicao_antiga_nome = serializers.CharField(source='refeicao_antiga.nome', read_only=True)
    refeicao_nova_nome = serializers.CharField(source='refeicao_nova.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrocaRefeicao
        fields = '__all__'
