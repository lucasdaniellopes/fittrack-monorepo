export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
  perfil?: {
    id: number;
    tipo: 'admin' | 'nutricionista' | 'personal' | 'cliente';
    telefone?: string;
    data_nascimento?: string;
  };
}

export interface Perfil {
  id: number;
  usuario: number;
  tipo: 'admin' | 'nutricionista' | 'personal' | 'cliente';
  telefone?: string;
  data_nascimento?: string;
  created_at: string;
  updated_at: string;
}

export interface TipoPlano {
  id: number;
  nome: string;
  descricao: string;
  preco: string;
  duracao_dias: number;
  intervalo_atualizacao_treino_dieta: number;
  limite_trocas_exercicios: number;
  limite_trocas_refeicoes: number;
  periodo_trocas_dias: number;
  trocas_ilimitadas: boolean;
}

export interface Cliente {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
  data_nascimento?: string;
  altura?: number;
  peso?: number;
  tipo_plano?: TipoPlano;
  data_inicio_plano?: string;
  data_fim_plano?: string;
  perfil?: Perfil;
  data_ultimo_treino?: string;
  data_ultima_dieta?: string;
  trocas_exercicios_restantes: number;
  trocas_refeicoes_restantes: number;
}

export interface Treino {
  id: number;
  nome: string;
  descricao: string;
  duracao: number;
  cliente: number;
  exercicios?: Exercicio[];
}

export interface Dieta {
  id: number;
  nome: string;
  descricao: string;
  calorias: number;
  cliente: number;
  refeicoes?: Refeicao[];
}

export interface Exercicio {
  id: number;
  nome: string;
  descricao: string;
  treino: number;
}

export interface Refeicao {
  id: number;
  nome: string;
  descricao: string;
  calorias: number;
  dieta: number;
}

export interface HistoricoTreino {
  id: number;
  cliente: number;
  treino: Treino;
  data_inicio: string;
  data_fim?: string;
  observacoes?: string;
}

export interface HistoricoDieta {
  id: number;
  cliente: number;
  dieta: Dieta;
  data_inicio: string;
  data_fim?: string;
  observacoes?: string;
}

export interface TrocaExercicio {
  id: number;
  cliente: number;
  exercicio_antigo: Exercicio;
  exercicio_novo: Exercicio;
  data_troca: string;
  motivo: string;
}

export interface TrocaRefeicao {
  id: number;
  cliente: number;
  refeicao_antiga: Refeicao;
  refeicao_nova: Refeicao;
  data_troca: string;
  motivo: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}