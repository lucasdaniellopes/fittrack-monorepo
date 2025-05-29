# Estrutura de Rotas da API FitTrack

## URLs Principais (Mantidas originais)

**Todas as rotas estão disponíveis em**: `api/v1/`

### 👥 Gestão de Usuários e Contas
- `api/v1/usuarios/` - Gestão de usuários
- `api/v1/perfis/` - Perfis de usuários
- `api/v1/tipos-plano/` - Tipos de planos
- `api/v1/clientes/` - Gestão de clientes
- `api/v1/personais/` - Personal trainers
- `api/v1/nutricionistas/` - Nutricionistas

### 💪 Treinos e Exercícios
- `api/v1/treinos/` - Gestão de treinos
- `api/v1/exercicios/` - Exercícios dos treinos
- `api/v1/historico-treinos/` - Histórico de treinos dos clientes
- `api/v1/trocas-exercicios/` - Solicitações de troca de exercícios

### 🥗 Nutrição e Dietas
- `api/v1/dietas/` - Gestão de dietas
- `api/v1/refeicoes/` - Refeições das dietas
- `api/v1/historico-dietas/` - Histórico de dietas dos clientes
- `api/v1/trocas-refeicoes/` - Solicitações de troca de refeições

### 📊 Relatórios e Notificações
- `api/v1/reports/` - Relatórios do sistema
- `api/v1/notifications/` - Sistema de notificações

## Autenticação
- `POST api/v1/auth/register/` - Registro de usuário
- `POST api/v1/token/` - Login (obter token)
- `POST api/v1/token/refresh/` - Renovar token

## Documentação
- `GET api/docs/` - Swagger UI
- `GET api/redoc/` - ReDoc
- `GET swagger/` - Redirecionamento para Swagger
- `GET docs/` - Redirecionamento para Swagger
- `GET redoc/` - Redirecionamento para ReDoc

## Arquitetura Modular

**🎯 O que mudou internamente:**
- Cada app agora tem sua própria estrutura `api/v1/`
- ViewSets organizados por domínio (accounts, nutrition, workouts, etc.)
- Core router importa e expõe ViewSets dos apps específicos
- **URLs mantidas exatamente iguais às originais**

**📁 Estrutura interna:**
```
accounts/api/v1/    → UserViewSet, ClienteViewSet, etc.
nutrition/api/v1/   → DietaViewSet, RefeicaoViewSet, etc.
workouts/api/v1/    → TreinoViewSet, ExercicioViewSet, etc.
reports/api/v1/     → BaseReportViewSet
notifications/api/v1/ → BaseNotificationViewSet
core/api/v1/        → Importa e expõe todos os ViewSets
```

**✅ Benefícios:**
- Código organizado por domínio
- Manutenção mais fácil
- URLs originais mantidas
- Compatibilidade total com código existente