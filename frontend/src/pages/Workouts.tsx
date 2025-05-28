import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Treino, Exercicio } from "@/types/types";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";
import api from "@/lib/api";
import { 
  Plus, 
  Search, 
  Dumbbell,
  Edit,
  Trash2,
  Eye,
  RefreshCcw
} from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const Workouts = () => {
  const [workouts, setWorkouts] = useState<Treino[]>([]);
  const [filteredWorkouts, setFilteredWorkouts] = useState<Treino[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [selectedWorkout, setSelectedWorkout] = useState<Treino | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [deleteWorkoutId, setDeleteWorkoutId] = useState<number | null>(null);
  const [editingWorkout, setEditingWorkout] = useState<Treino | null>(null);
  const [clientes, setClientes] = useState<any[]>([]);
  
  const { hasRole } = useAuth();
  const { toast } = useToast();
  
  const isTrainerOrAdmin = hasRole(["admin", "trainer"]);

  const [formData, setFormData] = useState({
    nome: "",
    descricao: "",
    duracao: 60,
    cliente: null as number | null
  });

  useEffect(() => {
    fetchWorkouts();
    fetchClientes();
  }, []);
  
  useEffect(() => {
    console.log("Estado dos clientes:", clientes);
  }, [clientes]);

  useEffect(() => {
    const filtered = workouts.filter((workout) => 
      workout.nome.toLowerCase().includes(searchQuery.toLowerCase()) ||
      workout.descricao.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredWorkouts(filtered);
  }, [searchQuery, workouts]);

  const fetchWorkouts = async () => {
    try {
      setIsLoading(true);
      const response = await api.get("treinos/");
      const data = response.data.results || response.data;
      setWorkouts(data);
      setFilteredWorkouts(data);
    } catch (error) {
      console.error("Erro ao carregar treinos:", error);
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao carregar treinos"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchClientes = async () => {
    try {
      const response = await api.get("clientes/");
      const data = response.data.results || response.data;
      console.log("Clientes carregados:", data);
      setClientes(data);
    } catch (error) {
      console.error("Erro ao carregar clientes:", error);
    }
  };

  const handleCreate = async () => {
    try {
      console.log("FormData antes de enviar:", formData);
      await api.post("treinos/", formData);
      toast({
        title: "Sucesso",
        description: "Treino criado com sucesso"
      });
      setIsCreateDialogOpen(false);
      setFormData({ nome: "", descricao: "", duracao: 60, cliente: null });
      fetchWorkouts();
    } catch (error) {
      console.error("Erro ao criar treino:", error);
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao criar treino"
      });
    }
  };

  const handleEdit = (workout: Treino) => {
    console.log("Editando workout:", workout);
    console.log("Cliente do workout:", workout.cliente);
    setEditingWorkout(workout);
    setFormData({
      nome: workout.nome,
      descricao: workout.descricao,
      duracao: workout.duracao,
      cliente: workout.cliente
    });
    setIsEditDialogOpen(true);
  };

  const handleUpdate = async () => {
    if (!editingWorkout) return;
    
    try {
      await api.patch(`treinos/${editingWorkout.id}/`, formData);
      toast({
        title: "Sucesso",
        description: "Treino atualizado com sucesso"
      });
      setIsEditDialogOpen(false);
      setEditingWorkout(null);
      setFormData({ nome: "", descricao: "", duracao: 60, cliente: null });
      fetchWorkouts();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao atualizar treino"
      });
    }
  };

  const handleDelete = async () => {
    if (!deleteWorkoutId) return;
    
    try {
      await api.delete(`treinos/${deleteWorkoutId}/`);
      toast({
        title: "Sucesso",
        description: "Treino excluído com sucesso"
      });
      setDeleteWorkoutId(null);
      fetchWorkouts();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao excluir treino"
      });
    }
  };

  const handleViewDetails = async (workout: Treino) => {
    try {
      const response = await api.get(`treinos/${workout.id}/`);
      setSelectedWorkout(response.data);
      setIsViewDialogOpen(true);
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao carregar detalhes do treino"
      });
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Carregando treinos...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Treinos</h1>
          <p className="text-muted-foreground">
            Visualize e gerencie seus planos de treino
          </p>
        </div>
        
        {isTrainerOrAdmin && (
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" /> 
            Criar Treino
          </Button>
        )}
      </div>
      
      <div className="flex items-center space-x-2">
        <Search className="h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar treinos..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="max-w-sm"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredWorkouts.map((workout) => (
          <Card key={workout.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Dumbbell className="h-5 w-5 text-primary" />
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleViewDetails(workout)}
                  >
                    <Eye className="h-4 w-4" />
                  </Button>
                  {isTrainerOrAdmin && (
                    <>
                      <Button variant="ghost" size="sm" onClick={() => handleEdit(workout)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setDeleteWorkoutId(workout.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </>
                  )}
                </div>
              </div>
              <CardTitle>{workout.nome}</CardTitle>
              <CardDescription>{workout.descricao}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>Duração: {workout.duracao} min</span>
                {workout.cliente_nome && (
                  <span>Cliente: {workout.cliente_nome}</span>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredWorkouts.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-8">
            <Dumbbell className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhum treino encontrado</h3>
            <p className="text-muted-foreground text-center mb-4">
              {searchQuery 
                ? "Nenhum treino corresponde aos seus critérios de busca."
                : "Comece criando seu primeiro treino."
              }
            </p>
            {searchQuery && (
              <Button variant="outline" onClick={() => setSearchQuery("")}>
                Limpar filtros
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Dialog de criação */}
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Novo Treino</DialogTitle>
            <DialogDescription>
              Crie um novo plano de treino
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="nome">Nome do Treino</Label>
              <Input
                id="nome"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                placeholder="Ex: Treino de Força"
              />
            </div>
            <div>
              <Label htmlFor="descricao">Descrição</Label>
              <Textarea
                id="descricao"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                placeholder="Descreva o objetivo do treino"
              />
            </div>
            <div>
              <Label htmlFor="duracao">Duração (minutos)</Label>
              <Input
                id="duracao"
                type="number"
                value={formData.duracao}
                onChange={(e) => setFormData({ ...formData, duracao: parseInt(e.target.value) })}
              />
            </div>
            <div>
              <Label htmlFor="cliente">Cliente ({clientes.length} disponíveis)</Label>
              <Select
                value={formData.cliente ? formData.cliente.toString() : undefined}
                onValueChange={(value) => {
                  console.log("Cliente selecionado (criar):", value);
                  setFormData({ ...formData, cliente: value ? parseInt(value) : null });
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um cliente" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="test">Teste</SelectItem>
                  {clientes.map((cliente) => (
                    <SelectItem key={cliente.id} value={cliente.id.toString()}>
                      {cliente.nome} - {cliente.email}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleCreate}>Criar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Dialog de edição */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Treino</DialogTitle>
            <DialogDescription>
              Edite os dados do treino
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="edit-nome">Nome do Treino</Label>
              <Input
                id="edit-nome"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                placeholder="Ex: Treino de Força"
              />
            </div>
            <div>
              <Label htmlFor="edit-descricao">Descrição</Label>
              <Textarea
                id="edit-descricao"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                placeholder="Descreva o objetivo do treino"
              />
            </div>
            <div>
              <Label htmlFor="edit-duracao">Duração (minutos)</Label>
              <Input
                id="edit-duracao"
                type="number"
                value={formData.duracao}
                onChange={(e) => setFormData({ ...formData, duracao: parseInt(e.target.value) })}
              />
            </div>
            <div>
              <Label htmlFor="edit-cliente">Cliente</Label>
              <Select
                value={formData.cliente ? formData.cliente.toString() : undefined}
                onValueChange={(value) => {
                  console.log("Cliente selecionado (editar):", value);
                  setFormData({ ...formData, cliente: value ? parseInt(value) : null });
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um cliente" />
                </SelectTrigger>
                <SelectContent>
                  {clientes.map((cliente) => (
                    <SelectItem key={cliente.id} value={cliente.id.toString()}>
                      {cliente.nome} - {cliente.email}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleUpdate}>Atualizar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Dialog de visualização */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{selectedWorkout?.nome}</DialogTitle>
            <DialogDescription>{selectedWorkout?.descricao}</DialogDescription>
          </DialogHeader>
          {selectedWorkout && (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground">
                  Duração: {selectedWorkout.duracao} minutos
                </p>
              </div>
              {selectedWorkout.exercicios && selectedWorkout.exercicios.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Exercícios:</h4>
                  <ul className="space-y-2">
                    {selectedWorkout.exercicios.map((exercicio: Exercicio) => (
                      <li key={exercicio.id} className="text-sm">
                        • {exercicio.nome} - {exercicio.descricao}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="flex justify-end gap-2 pt-4">
                {!isTrainerOrAdmin && (
                  <Button variant="outline">
                    <RefreshCcw className="mr-2 h-4 w-4" />
                    Solicitar Mudança
                  </Button>
                )}
                <Button onClick={() => setIsViewDialogOpen(false)}>
                  Fechar
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Alert de exclusão */}
      <AlertDialog open={!!deleteWorkoutId} onOpenChange={() => setDeleteWorkoutId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Você tem certeza?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta ação não pode ser desfeita. Isso excluirá permanentemente o treino.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              Excluir Treino
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default Workouts;