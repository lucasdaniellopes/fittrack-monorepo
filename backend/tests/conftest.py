"""
Pytest configuration and fixtures for the entire test suite.
This file is automatically discovered by pytest.
"""

import pytest
from django.conf import settings
from django.test import override_settings
from django.contrib.auth.models import User
from accounts.models import Perfil, Cliente, TipoPlano


# Django settings for testing
TEST_SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'PASSWORD_HASHERS': [
        'django.contrib.auth.hashers.MD5PasswordHasher',  # Faster for tests
    ],
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
    'CELERY_TASK_ALWAYS_EAGER': True,  # Execute celery tasks synchronously
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    },
}


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    """
    pass


@pytest.fixture
def test_settings():
    """Override Django settings for tests."""
    with override_settings(**TEST_SETTINGS):
        yield


@pytest.fixture
def test_user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Create an admin user."""
    user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        is_staff=True,
        is_superuser=True
    )
    # Update perfil to admin type
    perfil = Perfil.objects.get(usuario=user)
    perfil.tipo = Perfil.ADMIN
    perfil.save()
    return user


@pytest.fixture
def client_user():
    """Create a client user."""
    user = User.objects.create_user(
        username='client',
        email='client@example.com',
        password='clientpass123'
    )
    # Perfil is created automatically as CLIENTE
    return user


@pytest.fixture
def tipo_plano():
    """Create a test tipo plano."""
    return TipoPlano.objects.create(
        nome="Plano Teste",
        descricao="Plano para testes automatizados",
        preco="99.90",
        duracao_dias=30,
        limite_trocas_exercicios=5,
        limite_trocas_refeicoes=3,
        periodo_trocas_dias=7
    )


@pytest.fixture
def cliente(client_user, tipo_plano):
    """Create a test cliente."""
    perfil = Perfil.objects.get(usuario=client_user)
    return Cliente.objects.create(
        nome="Cliente Teste",
        email="cliente@test.com",
        perfil=perfil,
        tipo_plano=tipo_plano,
        altura=175,
        peso=70
    )


@pytest.fixture
def authenticated_client(client, admin_user):
    """Return an API client authenticated as admin."""
    from rest_framework_simplejwt.tokens import RefreshToken
    
    token = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client


@pytest.fixture
def api_client():
    """Return a DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, admin_user):
    """Return an authenticated DRF API client."""
    from rest_framework_simplejwt.tokens import RefreshToken
    
    token = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return api_client


@pytest.fixture
def sample_treino_data():
    """Return sample treino data for testing."""
    return {
        'nome': 'Treino Teste',
        'descricao': 'Descrição do treino de teste',
        'duracao': 60,
    }


@pytest.fixture
def sample_dieta_data():
    """Return sample dieta data for testing."""
    return {
        'nome': 'Dieta Teste',
        'descricao': 'Descrição da dieta de teste',
        'calorias': 2000,
    }


@pytest.fixture
def sample_exercicio_data():
    """Return sample exercicio data for testing."""
    return {
        'nome': 'Supino',
        'descricao': 'Exercício para desenvolvimento do peitoral',
    }


@pytest.fixture
def sample_refeicao_data():
    """Return sample refeicao data for testing."""
    return {
        'nome': 'Café da Manhã',
        'descricao': 'Primeira refeição do dia',
        'calorias': 300,
    }


# Pytest markers for categorizing tests
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (slower, with database)"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests (testing endpoints)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (can be skipped with -m 'not slow')"
    )
    config.addinivalue_line(
        "markers", "external: marks tests that require external services"
    )


# Custom pytest options
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--runslow", 
        action="store_true", 
        default=False, 
        help="run slow tests"
    )
    parser.addoption(
        "--runexternal", 
        action="store_true", 
        default=False, 
        help="run tests that require external services"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    skip_external = pytest.mark.skip(reason="need --runexternal option to run")
    
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
        if "external" in item.keywords and not config.getoption("--runexternal"):
            item.add_marker(skip_external)


# Database cleanup
@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up database after each test."""
    yield
    # Cleanup logic if needed
    pass