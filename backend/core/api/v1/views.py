from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from core.models import Perfil, Cliente
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer

@swagger_auto_schema(
    method='post',
    tags=['Auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password', 'first_name', 'last_name'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome de usuário único'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email do usuário'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nome'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Sobrenome'),
        }
    ),
    responses={
        201: openapi.Response(
            description='Usuário criado com sucesso',
            schema=UserSerializer
        ),
        400: openapi.Response(
            description='Erro de validação',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registra um novo usuário cliente no sistema.
    """
    try:
        # Validação dos campos obrigatórios
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'detail': f'O campo {field} é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Verificar se o username já existe
        if User.objects.filter(username=request.data['username']).exists():
            return Response(
                {'detail': 'Este nome de usuário já está em uso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se o email já existe
        if User.objects.filter(email=request.data['email']).exists():
            return Response(
                {'detail': 'Este email já está cadastrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Criar o usuário
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )
        
        # O signal já cria o perfil automaticamente, então vamos apenas buscar
        # e garantir que seja do tipo cliente
        perfil = user.perfil
        if perfil.tipo != 'cliente':
            perfil.tipo = 'cliente'
            perfil.save()
        
        # O signal também já cria o Cliente, então vamos apenas atualizar se necessário
        if hasattr(perfil, 'cliente'):
            cliente = perfil.cliente
            # Atualizar informações do cliente se necessário
            cliente.nome = f"{user.first_name} {user.last_name}"
            cliente.email = user.email
            cliente.save()
        
        # Serializar e retornar o usuário criado
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Erro ao criar usuário: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )