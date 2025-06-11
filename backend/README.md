# FitTrack - Sistema de Gerenciamento de Treinos e Dietas

FitTrack é uma API RESTful para gerenciamento de treinos e dietas personalizados, desenvolvida com Django e Django REST Framework. O sistema permite que nutricionistas e personal trainers criem e gerenciem planos de treino e dieta para seus clientes, com diferentes níveis de planos de assinatura.

## Funcionalidades Principais

- **Autenticação JWT**: Sistema seguro de autenticação com tokens JWT
- **Gerenciamento de Usuários**: Administração de diferentes perfis (admin, nutricionista, personal, cliente)
- **Planos de Assinatura**: Diferentes níveis de planos com regras de negócio específicas
- **Treinos Personalizados**: Criação e gerenciamento de treinos com exercícios vinculados a clientes específicos
- **Dietas Personalizadas**: Criação e gerenciamento de dietas com refeições vinculadas a clientes específicos
- **Sistema de Trocas**: Permite aos clientes solicitar trocas de exercícios e refeições conforme seu plano
- **Histórico Automático**: Registro automático de histórico de treinos e dietas para acompanhamento da evolução

## Planos Disponíveis

### Plano Básico
- **Preço**: R$ 59,90 por mês
- **Intervalo de atualização de treino/dieta**: 30 dias
- **Limite de trocas**: 1 exercício e 1 refeição
- **Período para trocas**: 3 dias após receber treino/dieta
- **Trocas ilimitadas**: Não

### Plano Pro
- **Preço**: R$ 129,90 por mês
- **Intervalo de atualização de treino/dieta**: 7 dias (semanal)
- **Limite de trocas**: 5 exercícios e 5 refeições
- **Período para trocas**: 7 dias após receber treino/dieta
- **Trocas ilimitadas**: Sim

## Tecnologias Utilizadas

- **Django**: 5.1.7
- **Django REST Framework**: 3.15.2
- **djangorestframework_simplejwt**: 5.5.0
- **drf-yasg**: 1.21.7 (Documentação Swagger/ReDoc)
- **PostgreSQL**: Banco de dados relacional
- **Python Decouple**: Para configurações de ambiente

## Requisitos

- Python 3.8+
- PostgreSQL
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/FitTrack.git
   cd FitTrack
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com suas variáveis de ambiente (use `.env.example` como base)

5. Execute as migrações:
   ```
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```

7. Inicie o servidor:
   ```
   python manage.py runserver
   ```

## Estrutura do Projeto

- **FitTrack/**: Configurações principais do projeto Django
- **core/**: Aplicação principal com modelos, views e lógica de negócio
  - **api/v1/**: Endpoints da API versão 1
    - **viewsets.py**: ViewSets para os recursos da API
    - **serializers.py**: Serializers para conversão de dados
    - **permissions.py**: Classes de permissão personalizadas
    - **routers.py**: Configuração de rotas da API

## Modelo de Dados

O FitTrack implementa um modelo de dados que garante a personalização completa de treinos e dietas:

- **Treinos pertencem a Clientes**: Cada treino é vinculado a um cliente específico
- **Dietas pertencem a Clientes**: Cada dieta é vinculada a um cliente específico
- **Exercícios pertencem a Treinos**: Cada exercício está vinculado a um treino específico
- **Refeições pertencem a Dietas**: Cada refeição está vinculada a uma dieta específica
- **Histórico Automático**: Ao criar um novo treino ou dieta, um registro é automaticamente adicionado ao histórico

## Documentação da API

A documentação da API está disponível nos seguintes endpoints:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Testes com Postman

O projeto inclui uma collection do Postman para testar todos os endpoints da API:

1. Importe o arquivo `FitTrack_Postman_Collection.json` no Postman
2. Importe o arquivo `FitTrack_Postman_Environment.json` para configurar as variáveis de ambiente
3. Configure a variável `base_url` no ambiente do Postman
4. Use a requisição "Obter Token" para autenticar e iniciar os testes

## Sistema de Permissões

O FitTrack implementa um sistema de controle de acesso baseado em papéis (RBAC):

- **Admin**: Acesso completo a todas as funcionalidades
- **Nutricionista**: Gerencia dietas e refeições
- **Personal**: Gerencia treinos e exercícios
- **Cliente**: Visualiza seus treinos e dietas, solicita trocas conforme seu plano


## 🧪 Executando Testes

### Instalação das Dependências de Teste
```bash
pip install -r requirements-test.txt
```

### Executar Todos os Testes
```bash
python manage.py test core.tests --verbosity=2
```

### Testes por Categoria
```bash
# Testes de API
python manage.py test core.tests.test_api_views

# Testes de Modelos  
python manage.py test core.tests.test_models

# Testes de Permissões
python manage.py test core.tests.test_permissions

# Testes de Signals
python manage.py test core.tests.test_signals
```


## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request


