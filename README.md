# FitTrack

Sistema completo de gerenciamento de treinos e dietas personalizados para academias, nutricionistas e personal trainers.

## 📋 Sobre o Projeto

FitTrack é uma plataforma que permite que profissionais de saúde e fitness criem e gerenciem planos de treino e dietas personalizados para seus clientes. O sistema oferece diferentes níveis de assinatura com funcionalidades específicas para cada tipo de plano.

### Principais Funcionalidades

- **Gestão de Usuários**: Sistema multi-perfil (Admin, Nutricionista, Personal Trainer, Cliente)
- **Planos de Assinatura**: Básico (R$ 59,90) e Pro (R$ 129,90)
- **Treinos Personalizados**: Criação e gestão de exercícios customizados
- **Dietas Personalizadas**: Planejamento nutricional individualizado
- **Sistema de Trocas**: Permite substituições de exercícios/refeições conforme o plano
- **Histórico Automático**: Registro completo de treinos e dietas anteriores
- **Dashboard Analítico**: Visualização de estatísticas e progresso

## 🚀 Tecnologias

### Backend
- **Django 5.1.7** - Framework web Python
- **Django REST Framework 3.15.2** - API REST
- **PostgreSQL** - Banco de dados
- **JWT** - Autenticação via tokens
- **drf-yasg** - Documentação automática da API (Swagger/ReDoc)

### Frontend
- **React 18.3.1** - Biblioteca JavaScript
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **Shadcn/ui** - Componentes UI
- **React Router DOM** - Roteamento
- **React Query** - Gerenciamento de estado
- **React Hook Form + Zod** - Formulários e validação

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Backend

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/FitTrack.git
cd FitTrack
```

2. Configure o ambiente virtual e instale as dependências:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` no diretório `backend/` com:
```env
SECRET_KEY=sua-secret-key
DEBUG=True
DATABASE_URL=postgres://usuario:senha@localhost:5432/fittrack
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

### Frontend

1. Em outro terminal, navegue até o diretório frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
# ou
yarn install
# ou
bun install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
# ou
yarn dev
# ou
bun dev
```

## 📝 Documentação da API

Com o servidor backend rodando, acesse:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### Coleção Postman

O projeto inclui uma coleção Postman para testes da API:
- `backend/FitTrack_Postman_Collection.json`
- `backend/FitTrack_Postman_Environment.json`

## 🔐 Autenticação

O sistema utiliza JWT (JSON Web Tokens) para autenticação. Após o login, o token deve ser incluído no header das requisições:

```
Authorization: Bearer {seu-token-jwt}
```

## 📊 Estrutura de Planos

### Plano Básico (R$ 59,90)
- ✅ Acesso aos treinos e dietas
- ✅ Histórico de treinos e dietas
- ❌ Troca de exercícios
- ❌ Personalização de dietas

### Plano Pro (R$ 129,90)
- ✅ Todas as funcionalidades do plano Básico
- ✅ Troca ilimitada de exercícios
- ✅ Personalização completa de dietas
- ✅ Suporte prioritário

## 🗂️ Estrutura do Projeto

```
FitTrack/
├── backend/
│   ├── FitTrack/         # Configurações do Django
│   ├── core/             # App principal
│   │   ├── api/v1/       # Endpoints da API
│   │   ├── models.py     # Modelos do banco
│   │   └── migrations/   # Migrações do banco
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/   # Componentes React
    │   ├── pages/        # Páginas da aplicação
    │   ├── contexts/     # Context API
    │   ├── hooks/        # Custom hooks
    │   ├── lib/          # Utilitários
    │   └── types/        # TypeScript types
    ├── package.json
    └── vite.config.ts
```

## 👥 Perfis de Usuário

- **Administrador**: Acesso total ao sistema
- **Nutricionista**: Criação e gestão de dietas
- **Personal Trainer**: Criação e gestão de treinos
- **Cliente**: Visualização de seus treinos e dietas

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através de [seu-email@exemplo.com](mailto:seu-email@exemplo.com)