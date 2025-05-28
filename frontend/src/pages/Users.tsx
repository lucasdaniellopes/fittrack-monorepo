import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Plus, Search, Edit, Trash2, User as UserIcon } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import api from "@/lib/api";
import { User } from "@/types/types";

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    telefone: "",
    data_nascimento: "",
    perfil_tipo: "cliente"
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    const filtered = users.filter(user =>
      user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.last_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredUsers(filtered);
  }, [searchTerm, users]);

  const fetchUsers = async () => {
    try {
      const response = await api.get("usuarios/");
      // A resposta está paginada, então precisamos acessar o array de resultados
      const usersData = response.data.results || response.data;
      setUsers(usersData);
      setFilteredUsers(usersData);
    } catch (error) {
      console.error("Erro ao carregar usuários:", error);
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao carregar usuários"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingUser) {
        // Atualizar usuário existente
        await api.patch(`usuarios/${editingUser.id}/`, {
          username: formData.username,
          email: formData.email,
          first_name: formData.first_name,
          last_name: formData.last_name,
          is_staff: formData.perfil_tipo === "admin"
        });

        // Atualizar perfil se existir
        if (editingUser.perfil) {
          await api.patch(`perfis/${editingUser.perfil.id}/`, {
            tipo: formData.perfil_tipo,
            telefone: formData.telefone || editingUser.perfil.telefone,
            data_nascimento: formData.data_nascimento || editingUser.perfil.data_nascimento
          });
        }

        toast({
          title: "Sucesso",
          description: "Usuário atualizado com sucesso"
        });
      } else {
        // Criar novo usuário
        const userResponse = await api.post("usuarios/", {
          username: formData.username,
          email: formData.email,
          first_name: formData.first_name,
          last_name: formData.last_name,
          password: formData.password,
          is_staff: formData.perfil_tipo === "admin",
          tipo_perfil: formData.perfil_tipo  // Envia o tipo de perfil desejado
        });

        // Atualizar perfil com telefone e data_nascimento se foram fornecidos
        if (formData.telefone || formData.data_nascimento) {
          // Buscar o perfil criado automaticamente
          const perfilResponse = await api.get("perfis/");
          const perfis = perfilResponse.data.results || perfilResponse.data;
          const userPerfil = perfis.find((p: any) => p.usuario === userResponse.data.id);
          
          if (userPerfil) {
            await api.patch(`perfis/${userPerfil.id}/`, {
              telefone: formData.telefone || userPerfil.telefone,
              data_nascimento: formData.data_nascimento || userPerfil.data_nascimento
            });
          }
        }

        toast({
          title: "Sucesso",
          description: "Usuário criado com sucesso"
        });
      }

      setIsDialogOpen(false);
      setEditingUser(null);
      resetForm();
      fetchUsers();
    } catch (error: any) {
      console.error("Erro ao salvar usuário:", error.response?.data);
      
      let errorMessage = "Erro ao salvar usuário";
      
      // Tratar erros específicos
      if (error.response?.data) {
        if (error.response.data.username) {
          errorMessage = error.response.data.username[0];
        } else if (error.response.data.email) {
          errorMessage = error.response.data.email[0];
        } else if (error.response.data.password) {
          errorMessage = error.response.data.password[0];
        } else if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.non_field_errors) {
          errorMessage = error.response.data.non_field_errors[0];
        }
      }
      
      toast({
        variant: "destructive",
        title: "Erro",
        description: errorMessage
      });
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      password: "",
      telefone: user.perfil?.telefone || "",
      data_nascimento: user.perfil?.data_nascimento || "",
      perfil_tipo: user.perfil?.tipo || "cliente"
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (user: User) => {
    if (!confirm("Tem certeza que deseja excluir este usuário?")) return;

    try {
      await api.delete(`usuarios/${user.id}/`);
      toast({
        title: "Sucesso",
        description: "Usuário excluído com sucesso"
      });
      fetchUsers();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao excluir usuário"
      });
    }
  };

  const resetForm = () => {
    setFormData({
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      telefone: "",
      data_nascimento: "",
      perfil_tipo: "cliente"
    });
  };

  const openCreateDialog = () => {
    setEditingUser(null);
    resetForm();
    setIsDialogOpen(true);
  };

  const getRoleLabel = (tipo: string) => {
    const roles = {
      admin: "Administrador",
      nutricionista: "Nutricionista", 
      personal: "Personal Trainer",
      cliente: "Cliente"
    };
    return roles[tipo as keyof typeof roles] || tipo;
  };

  const getRoleBadgeVariant = (tipo: string) => {
    switch (tipo) {
      case "admin": return "destructive";
      case "nutricionista": return "default";
      case "personal": return "secondary";
      case "cliente": return "outline";
      default: return "outline";
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando usuários...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Usuários</h1>
          <p className="text-muted-foreground">Gerencie os usuários do sistema</p>
        </div>
        
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={openCreateDialog}>
              <Plus className="mr-2 h-4 w-4" />
              Novo Usuário
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>
                {editingUser ? "Editar Usuário" : "Novo Usuário"}
              </DialogTitle>
              <DialogDescription>
                {editingUser 
                  ? "Edite as informações do usuário."
                  : "Preencha os dados para criar um novo usuário."
                }
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="username">Username</Label>
                  <Input
                    id="username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="first_name">Nome</Label>
                  <Input
                    id="first_name"
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="last_name">Sobrenome</Label>
                  <Input
                    id="last_name"
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    required
                  />
                </div>
              </div>

              {!editingUser && (
                <div>
                  <Label htmlFor="password">Senha</Label>
                  <Input
                    id="password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="perfil_tipo">Tipo de Perfil</Label>
                  <Select value={formData.perfil_tipo} onValueChange={(value) => setFormData({ ...formData, perfil_tipo: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cliente">Cliente</SelectItem>
                      <SelectItem value="personal">Personal Trainer</SelectItem>
                      <SelectItem value="nutricionista">Nutricionista</SelectItem>
                      <SelectItem value="admin">Administrador</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input
                    id="telefone"
                    value={formData.telefone}
                    onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="data_nascimento">Data de Nascimento</Label>
                <Input
                  id="data_nascimento"
                  type="date"
                  value={formData.data_nascimento}
                  onChange={(e) => setFormData({ ...formData, data_nascimento: e.target.value })}
                />
              </div>


              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingUser ? "Atualizar" : "Criar"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex items-center space-x-2">
        <Search className="h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar usuários..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-sm"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {Array.isArray(filteredUsers) && filteredUsers.map((user) => (
          <Card key={user.id} className="relative">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <UserIcon className="h-5 w-5 text-muted-foreground" />
                  <CardTitle className="text-lg">{user.username}</CardTitle>
                </div>
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleEdit(user)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(user)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <CardDescription className="text-sm">
                {user.first_name} {user.last_name}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div>
                  <p className="text-sm text-muted-foreground">Email:</p>
                  <p className="text-sm">{user.email}</p>
                </div>
                
                {user.perfil && (
                  <>
                    <div>
                      <p className="text-sm text-muted-foreground">Perfil:</p>
                      <Badge variant={getRoleBadgeVariant(user.perfil.tipo) as any}>
                        {getRoleLabel(user.perfil.tipo)}
                      </Badge>
                    </div>
                    
                    {user.perfil?.telefone && (
                      <div>
                        <p className="text-sm text-muted-foreground">Telefone:</p>
                        <p className="text-sm">{user.perfil.telefone}</p>
                      </div>
                    )}
                    
                    {user.perfil?.data_nascimento && (
                      <div>
                        <p className="text-sm text-muted-foreground">Nascimento:</p>
                        <p className="text-sm">
                          {new Date(user.perfil.data_nascimento).toLocaleDateString('pt-BR')}
                        </p>
                      </div>
                    )}
                  </>
                )}
                
                <div className="flex justify-between items-center text-xs text-muted-foreground pt-2">
                  <span>Ativo: {user.is_active ? "Sim" : "Não"}</span>
                  {user.is_staff && <Badge variant="destructive" className="text-xs">Admin</Badge>}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {(!Array.isArray(filteredUsers) || filteredUsers.length === 0) && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-8">
            <UserIcon className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhum usuário encontrado</h3>
            <p className="text-muted-foreground text-center mb-4">
              {searchTerm 
                ? "Tente ajustar sua busca ou criar um novo usuário."
                : "Comece criando seu primeiro usuário."
              }
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Users;