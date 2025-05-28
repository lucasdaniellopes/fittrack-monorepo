import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import api from '../lib/api';
import type { User, Perfil, LoginCredentials, AuthTokens } from '../types/types';

interface AuthContextType {
  user: User | null;
  perfil: Perfil | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  loading: boolean; // alias para compatibilidade
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  hasRole: (roles: string | string[]) => boolean;
  checkTokenExpiration: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [perfil, setPerfil] = useState<Perfil | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          try {
            const userResponse = await api.get('/usuarios/me/');
            setUser(userResponse.data);
            
            // Buscar perfil do usuário
            try {
              const perfilResponse = await api.get('/perfis/');
              console.log('Perfil Response:', perfilResponse.data);
              const perfis = perfilResponse.data.results || perfilResponse.data;
              
              // For non-staff users, the API only returns their own perfil
              let userPerfil = null;
              if (userResponse.data.is_staff) {
                userPerfil = perfis.find((p: Perfil) => p.usuario === userResponse.data.id);
              } else if (perfis.length > 0) {
                // For regular users, take the first (and only) perfil
                userPerfil = perfis[0];
              }
              
              console.log('Found user perfil:', userPerfil);
              if (userPerfil) {
                setPerfil(userPerfil);
              } else {
                console.error('No perfil found for user:', userResponse.data.id);
              }
            } catch (error) {
              console.error('Erro ao buscar perfil:', error);
            }
          } catch (error: any) {
            console.error('Error loading user:', error.response?.status, error.response?.data);
            if (error.response?.status === 401) {
              // Token inválido ou expirado
              try {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
              } catch (e) {
                // Ignore storage errors
              }
            }
          }
        }
      } catch (error) {
        console.error('Storage access error:', error);
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await api.post<AuthTokens>('/token/', credentials);
      const { access, refresh } = response.data;
      
      try {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
      } catch (e) {
        console.error('Cannot store tokens:', e);
      }
      
      const userResponse = await api.get('/usuarios/me/');
      setUser(userResponse.data);
      
      // Buscar perfil do usuário
      try {
        const perfilResponse = await api.get('/perfis/');
        console.log('Login - Perfil Response:', perfilResponse.data);
        const perfis = perfilResponse.data.results || perfilResponse.data;
        
        // For non-staff users, the API only returns their own perfil
        let userPerfil = null;
        if (userResponse.data.is_staff) {
          userPerfil = perfis.find((p: Perfil) => p.usuario === userResponse.data.id);
        } else if (perfis.length > 0) {
          // For regular users, take the first (and only) perfil
          userPerfil = perfis[0];
        }
        
        console.log('Login - Found user perfil:', userPerfil);
        if (userPerfil) {
          setPerfil(userPerfil);
        } else {
          console.error('Login - No perfil found for user:', userResponse.data.id);
        }
      } catch (error) {
        console.error('Erro ao buscar perfil:', error);
      }
    } catch (error: any) {
      console.error('Login error:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao fazer login');
    }
  };

  const logout = () => {
    try {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (e) {
      // Ignore storage errors
    }
    setUser(null);
    setPerfil(null);
  };

  const hasRole = (roles: string | string[]) => {
    console.log("hasRole Debug:", {
      roles,
      user: user?.username,
      is_staff: user?.is_staff,
      perfil,
      perfilTipo: perfil?.tipo
    });
    
    if (!user) return false;
    
    // Para usuários com is_staff, sempre retornar true para role admin
    if (user.is_staff && (roles === 'admin' || (Array.isArray(roles) && roles.includes('admin')))) {
      return true;
    }
    
    if (!perfil) return false;
    
    // Map old role names to new ones for compatibility
    const roleMap: Record<string, string> = {
      'admin': 'admin',
      'nutritionist': 'nutricionista',
      'trainer': 'personal',
      'client': 'cliente'
    };
    
    const userRole = perfil.tipo;
    
    if (Array.isArray(roles)) {
      const result = roles.some(role => {
        const mappedRole = roleMap[role] || role;
        console.log(`Checking role: ${role} -> ${mappedRole} against userRole: ${userRole}`);
        return userRole === mappedRole;
      });
      console.log("hasRole result:", result);
      return result;
    }
    
    const mappedRole = roleMap[roles] || roles;
    const result = userRole === mappedRole;
    console.log(`Single role check: ${roles} -> ${mappedRole} against userRole: ${userRole}, result: ${result}`);
    return result;
  };

  const checkTokenExpiration = () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return false;
      
      // Decode JWT token to check expiration
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp * 1000; // Convert to milliseconds
      return Date.now() < exp;
    } catch (error) {
      return false;
    }
  };

  // Create a compatible user object
  const compatibleUser = user ? {
    ...user,
    name: user.first_name && user.last_name 
      ? `${user.first_name} ${user.last_name}`.trim() 
      : user.username,
    role: user.is_staff ? 'admin' : (perfil?.tipo || 'cliente')
  } : null;

  const value = {
    user: compatibleUser as any,
    perfil,
    isAuthenticated: !!user,
    isLoading,
    loading: isLoading, // alias para compatibilidade
    login,
    logout,
    hasRole,
    checkTokenExpiration,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};