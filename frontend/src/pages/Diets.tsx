import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Dieta, Refeicao } from "@/types/types";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";
import api from "@/lib/api";
import { 
  Plus, 
  Search, 
  Utensils,
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

const Diets = () => {
  const [diets, setDiets] = useState<Dieta[]>([]);
  const [filteredDiets, setFilteredDiets] = useState<Dieta[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [selectedDiet, setSelectedDiet] = useState<Dieta | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [deleteDietId, setDeleteDietId] = useState<number | null>(null);
  const [editingDiet, setEditingDiet] = useState<Dieta | null>(null);
  const [clientes, setClientes] = useState<any[]>([]);
  
  const { hasRole } = useAuth();
  const { toast } = useToast();
  
  const isNutritionistOrAdmin = hasRole(["admin", "nutritionist"]);

  const [formData, setFormData] = useState({
    nome: "",
    descricao: "",
    calorias: 2000,
    cliente: null as number | null
  });

  useEffect(() => {
    fetchDiets();
    fetchClientes();
  }, []);

  useEffect(() => {
    const filtered = diets.filter((diet) => 
      diet.nome.toLowerCase().includes(searchQuery.toLowerCase()) ||
      diet.descricao.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredDiets(filtered);
  }, [searchQuery, diets]);

  const fetchDiets = async () => {
    try {
      setIsLoading(true);
      const response = await api.get("dietas/");
      const data = response.data.results || response.data;
      setDiets(data);
      setFilteredDiets(data);
    } catch (error) {
      console.error("Erro ao carregar dietas:", error);
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao carregar dietas"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchClientes = async () => {
    try {
      const response = await api.get("clientes/");
      const data = response.data.results || response.data;
      console.log("Clientes carregados (Dietas):", data);
      setClientes(data);
    } catch (error) {
      console.error("Erro ao carregar clientes:", error);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post("dietas/", formData);
      toast({
        title: "Sucesso",
        description: "Dieta criada com sucesso"
      });
      setIsCreateDialogOpen(false);
      setFormData({ nome: "", descricao: "", calorias: 2000, cliente: null });
      fetchDiets();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao criar dieta"
      });
    }
  };

  const handleEdit = (diet: Dieta) => {
    setEditingDiet(diet);
    setFormData({
      nome: diet.nome,
      descricao: diet.descricao,
      calorias: diet.calorias,
      cliente: diet.cliente
    });
    setIsEditDialogOpen(true);
  };

  const handleUpdate = async () => {
    if (!editingDiet) return;
    
    try {
      await api.patch(`dietas/${editingDiet.id}/`, formData);
      toast({
        title: "Sucesso",
        description: "Dieta atualizada com sucesso"
      });
      setIsEditDialogOpen(false);
      setEditingDiet(null);
      setFormData({ nome: "", descricao: "", calorias: 2000, cliente: null });
      fetchDiets();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao atualizar dieta"
      });
    }
  };

  const handleDelete = async () => {
    if (!deleteDietId) return;
    
    try {
      await api.delete(`dietas/${deleteDietId}/`);
      toast({
        title: "Sucesso",
        description: "Dieta excluída com sucesso"
      });
      setDeleteDietId(null);
      fetchDiets();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao excluir dieta"
      });
    }
  };

  const handleViewDetails = async (diet: Dieta) => {
    try {
      const response = await api.get(`dietas/${diet.id}/`);
      setSelectedDiet(response.data);
      setIsViewDialogOpen(true);
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Erro ao carregar detalhes da dieta"
      });
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Carregando dietas...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Dietas</h1>
          <p className="text-muted-foreground">
            Visualize e gerencie seus planos de dieta
          </p>
        </div>
        
        {isNutritionistOrAdmin && (
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" /> 
            Criar Dieta
          </Button>
        )}
      </div>
      
      <div className="flex items-center space-x-2">
        <Search className="h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar dietas..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="max-w-sm"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredDiets.map((diet) => (
          <Card key={diet.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Utensils className="h-5 w-5 text-primary" />
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleViewDetails(diet)}
                  >
                    <Eye className="h-4 w-4" />
                  </Button>
                  {isNutritionistOrAdmin && (
                    <>
                      <Button variant="ghost" size="sm" onClick={() => handleEdit(diet)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setDeleteDietId(diet.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </>
                  )}
                </div>
              </div>
              <CardTitle>{diet.nome}</CardTitle>
              <CardDescription>{diet.descricao}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>{diet.calorias} kcal</span>
                {diet.cliente_nome && (
                  <span>Cliente: {diet.cliente_nome}</span>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredDiets.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-8">
            <Utensils className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhuma dieta encontrada</h3>
            <p className="text-muted-foreground text-center mb-4">
              {searchQuery 
                ? "Nenhuma dieta corresponde aos seus critérios de busca."
                : "Comece criando sua primeira dieta."
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
            <DialogTitle>Nova Dieta</DialogTitle>
            <DialogDescription>
              Crie um novo plano de dieta
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="nome">Nome da Dieta</Label>
              <Input
                id="nome"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                placeholder="Ex: Dieta Rica em Proteína"
              />
            </div>
            <div>
              <Label htmlFor="descricao">Descrição</Label>
              <Textarea
                id="descricao"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                placeholder="Descreva o objetivo da dieta"
              />
            </div>
            <div>
              <Label htmlFor="calorias">Calorias Totais</Label>
              <Input
                id="calorias"
                type="number"
                value={formData.calorias}
                onChange={(e) => setFormData({ ...formData, calorias: parseInt(e.target.value) })}
              />
            </div>
            <div>
              <Label htmlFor="cliente">Cliente</Label>
              <Select
                value={formData.cliente?.toString() || ""}
                onValueChange={(value) => setFormData({ ...formData, cliente: parseInt(value) })}
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
            <DialogTitle>Editar Dieta</DialogTitle>
            <DialogDescription>
              Edite os dados da dieta
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="edit-nome">Nome da Dieta</Label>
              <Input
                id="edit-nome"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                placeholder="Ex: Dieta Rica em Proteína"
              />
            </div>
            <div>
              <Label htmlFor="edit-descricao">Descrição</Label>
              <Textarea
                id="edit-descricao"
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                placeholder="Descreva o objetivo da dieta"
              />
            </div>
            <div>
              <Label htmlFor="edit-calorias">Calorias Totais</Label>
              <Input
                id="edit-calorias"
                type="number"
                value={formData.calorias}
                onChange={(e) => setFormData({ ...formData, calorias: parseInt(e.target.value) })}
              />
            </div>
            <div>
              <Label htmlFor="edit-cliente">Cliente</Label>
              <Select
                value={formData.cliente?.toString() || ""}
                onValueChange={(value) => setFormData({ ...formData, cliente: parseInt(value) })}
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
            <DialogTitle>{selectedDiet?.nome}</DialogTitle>
            <DialogDescription>{selectedDiet?.descricao}</DialogDescription>
          </DialogHeader>
          {selectedDiet && (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground">
                  Calorias totais: {selectedDiet.calorias} kcal
                </p>
              </div>
              {selectedDiet.refeicoes && selectedDiet.refeicoes.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-2">Refeições:</h4>
                  <ul className="space-y-2">
                    {selectedDiet.refeicoes.map((refeicao: Refeicao) => (
                      <li key={refeicao.id} className="text-sm">
                        • {refeicao.nome} - {refeicao.calorias} kcal
                        <p className="text-xs text-muted-foreground ml-4">{refeicao.descricao}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="flex justify-end gap-2 pt-4">
                {!isNutritionistOrAdmin && (
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
      <AlertDialog open={!!deleteDietId} onOpenChange={() => setDeleteDietId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Você tem certeza?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta ação não pode ser desfeita. Isso excluirá permanentemente a dieta.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              Excluir Dieta
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default Diets;