# FitTrack Backend - Guia de Testes

Este documento descreve a estrutura de testes do backend FitTrack e como executá-los.

## 📁 Estrutura de Testes

```
backend/
├── tests/                     # Utilitários e configurações globais
│   ├── __init__.py
│   ├── test_utils.py          # Classes base e utilities
│   └── conftest.py            # Configurações pytest
├── core/tests/                # Testes do app core
│   ├── __init__.py
│   ├── test_models.py         # Testes de modelos base
│   ├── test_factories.py      # Testes do Factory Pattern
│   ├── test_strategies.py     # Testes do Strategy Pattern
│   ├── test_observers.py      # Testes do Observer Pattern
│   └── test_commands.py       # Testes do Command Pattern
├── accounts/tests/            # Testes do app accounts
│   ├── __init__.py
│   ├── test_models.py         # Testes de Perfil, Cliente, TipoPlano
│   ├── test_viewsets.py       # Testes de API endpoints
│   └── test_serializers.py    # Testes de serializers
├── workouts/tests/            # Testes do app workouts
│   ├── __init__.py
│   ├── test_models.py         # Testes de Treino, Exercicio, etc.
│   ├── test_viewsets.py       # Testes de API endpoints
│   └── test_serializers.py    # Testes de serializers
├── nutrition/tests/           # Testes do app nutrition
│   ├── __init__.py
│   ├── test_models.py         # Testes de Dieta, Refeicao, etc.
│   ├── test_viewsets.py       # Testes de API endpoints
│   └── test_serializers.py    # Testes de serializers
├── pytest.ini                # Configuração pytest
├── test_runner.py             # Script personalizado para executar testes
└── README_TESTS.md           # Este arquivo
```

## 🧪 Tipos de Testes

### 1. **Testes de Modelos** (`test_models.py`)
- Criação e validação de objetos
- Métodos `__str__` e propriedades
- Relacionamentos entre modelos
- Soft delete e campos de auditoria

### 2. **Testes de ViewSets** (`test_viewsets.py`)
- Endpoints de API (GET, POST, PUT, PATCH, DELETE)
- Autenticação e autorização
- Estrutura de resposta
- Filtros e paginação

### 3. **Testes de Serializers** (`test_serializers.py`)
- Serialização de dados
- Validações customizadas
- Campos calculados
- Criação e atualização via API

### 4. **Testes de Design Patterns**
- **Factory Pattern**: Criação de perfis
- **Strategy Pattern**: Estratégias de permissão
- **Observer Pattern**: Sistema de eventos
- **Command Pattern**: Comandos de troca

## 🚀 Como Executar os Testes

### Método 1: Script Personalizado (Recomendado)

```bash
# Executar todos os testes
python test_runner.py all

# Executar apenas testes unitários
python test_runner.py unit

# Executar testes com pytest
python test_runner.py pytest

# Executar testes com cobertura
python test_runner.py coverage

# Executar testes de um app específico
python test_runner.py app accounts

# Executar testes de API apenas
python test_runner.py api

# Executar testes rápidos (sem testes lentos)
python test_runner.py fast

# Ver estrutura de testes
python test_runner.py structure

# Verificar qualidade do código
python test_runner.py lint

# Formatar código automaticamente
python test_runner.py format
```

### Método 2: Django Test Runner

```bash
# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test accounts

# Executar teste específico
python manage.py test accounts.tests.test_models.PerfilModelTest

# Executar com paralelização
python manage.py test --parallel

# Manter banco de dados entre execuções
python manage.py test --keepdb
```

### Método 3: Pytest

```bash
# Executar todos os testes
pytest

# Executar com verbosidade
pytest -v

# Executar testes marcados
pytest -m api          # Apenas testes de API
pytest -m unit         # Apenas testes unitários
pytest -m integration  # Apenas testes de integração

# Executar testes específicos
pytest accounts/tests/test_models.py
pytest accounts/tests/test_models.py::PerfilModelTest::test_perfil_creation

# Executar com cobertura
pytest --cov=. --cov-report=html
```

## 📊 Cobertura de Testes

Para gerar relatório de cobertura:

```bash
# Com o script personalizado
python test_runner.py coverage

# Manualmente
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML em htmlcov/
```

## 🛠 Utilitários de Teste

### Classes Base

```python
from tests.test_utils import BaseTestCase, BaseAPITestCase

class MyModelTest(BaseTestCase):
    # Herda setup comum (user, perfil, cliente, tipo_plano)
    pass

class MyAPITest(BaseAPITestCase):
    # Herda setup de API (tokens JWT, autenticação)
    
    def test_endpoint(self):
        self.authenticate_as_admin()
        response = self.client.get('/api/v1/endpoint/')
        # ...
```

### Factory de Dados

```python
from tests.test_utils import TestDataFactory

# Criar dados de teste facilmente
user = TestDataFactory.create_user('novo_usuario')
tipo_plano = TestDataFactory.create_tipo_plano('Plano Premium')
cliente = TestDataFactory.create_cliente('Cliente Novo', user, tipo_plano)
```

### Fixtures Pytest

```python
def test_with_fixtures(cliente, tipo_plano, authenticated_api_client):
    # cliente, tipo_plano e api client já estão configurados
    response = authenticated_api_client.get('/api/v1/clientes/')
    assert response.status_code == 200
```

## 🔧 Configuração de Ambiente

### Variáveis de Ambiente para Testes

```bash
# .env.test (opcional)
DEBUG=False
DATABASE_URL=sqlite:///:memory:
SECRET_KEY=test-secret-key
```

### Configurações Django para Testes

As configurações são automaticamente otimizadas para testes:
- Banco SQLite em memória
- Password hasher rápido (MD5)
- Email backend em memória
- Cache em memória

## 📝 Convenções de Testes

### Nomenclatura

- **Arquivos**: `test_*.py`
- **Classes**: `*Test` ou `*TestCase`
- **Métodos**: `test_*`

### Estrutura de Teste

```python
class ModelTest(TestCase):
    def setUp(self):
        # Configuração inicial
        pass
    
    def test_model_creation(self):
        # Testar criação do modelo
        obj = Model.objects.create(...)
        self.assertEqual(obj.field, expected_value)
    
    def test_model_str_representation(self):
        # Testar representação string
        obj = Model(...)
        self.assertEqual(str(obj), expected_string)
    
    def test_model_validation(self):
        # Testar validações
        with self.assertRaises(ValidationError):
            Model.objects.create(invalid_data)
```

### Marcadores Pytest

- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.api` - Testes de API
- `@pytest.mark.slow` - Testes lentos
- `@pytest.mark.external` - Requer serviços externos

## 🐛 Debugging de Testes

### Executar Teste Específico

```bash
# Django
python manage.py test accounts.tests.test_models.PerfilModelTest.test_perfil_creation

# Pytest
pytest accounts/tests/test_models.py::PerfilModelTest::test_perfil_creation -v -s
```

### Debug com PDB

```python
def test_something(self):
    import pdb; pdb.set_trace()
    # Seu código de teste aqui
```

### Logs Detalhados

```bash
# Habilitar logs Django
python manage.py test --debug-mode

# Pytest com logs
pytest -v -s --log-cli-level=DEBUG
```

## 📈 Métricas de Qualidade

### Cobertura Mínima Esperada
- **Modelos**: 95%+
- **ViewSets**: 90%+
- **Serializers**: 90%+
- **Utilities**: 85%+

### Comandos Úteis

```bash
# Contar linhas de teste
find . -name "test_*.py" -exec wc -l {} + | sort -n

# Verificar testes que falharam recentemente
pytest --lf  # last failed

# Executar apenas testes modificados
pytest --testmon

# Profile de performance dos testes
pytest --durations=10
```

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de IntegrityError**: Conflito com signals automáticos
   - Usar `Perfil.objects.get(usuario=user)` em vez de criar
   
2. **Testes lentos**: 
   - Usar `--keepdb` para manter banco entre execuções
   - Marcar testes lentos com `@pytest.mark.slow`

3. **Problemas de importação**:
   - Verificar `__init__.py` em todas as pastas
   - Usar imports absolutos

4. **Falha de autenticação em API tests**:
   - Verificar se JWT tokens estão sendo gerados corretamente
   - Usar fixtures `authenticated_api_client`

### Performance Tips

- Use `--parallel` para testes Django
- Configure banco em memória para pytest
- Use fixtures em vez de setup repetitivo
- Marque testes externos para execução opcional

---

## 📚 Recursos Adicionais

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)