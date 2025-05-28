
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { useAuth } from "@/contexts/AuthContext";
import { Dumbbell, Utensils, Clock, RefreshCw, CheckCircle, XCircle, Loader2 } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import api from "@/lib/api";
import { TrocaExercicio, TrocaRefeicao, Treino, Dieta } from "@/types/types";
import { useToast } from "@/hooks/use-toast";

interface ChangeRequest {
  id: number;
  type: 'workout' | 'diet';
  cliente: number;
  clienteName?: string;
  data_troca: string;
  motivo: string;
  status?: 'pending' | 'approved' | 'rejected';
  exercicio_antigo?: any;
  exercicio_novo?: any;
  refeicao_antiga?: any;
  refeicao_nova?: any;
}

const Changes = () => {
  const { user, hasRole } = useAuth();
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState("all");
  const [changeType, setChangeType] = useState("workout");
  const [reason, setReason] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [itemToChange, setItemToChange] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [exerciseChanges, setExerciseChanges] = useState<TrocaExercicio[]>([]);
  const [mealChanges, setMealChanges] = useState<TrocaRefeicao[]>([]);
  const [workouts, setWorkouts] = useState<Treino[]>([]);
  const [diets, setDiets] = useState<Dieta[]>([]);
  
  const isProfessional = hasRole(["admin", "trainer", "nutritionist"]);

  useEffect(() => {
    fetchChanges();
    if (!isProfessional) {
      fetchUserItems();
    }
  }, []);

  const fetchChanges = async () => {
    try {
      setLoading(true);
      const [exerciseRes, mealRes] = await Promise.all([
        api.get("trocas-exercicios/"),
        api.get("trocas-refeicoes/")
      ]);
      setExerciseChanges(Array.isArray(exerciseRes.data) ? exerciseRes.data : []);
      setMealChanges(Array.isArray(mealRes.data) ? mealRes.data : []);
    } catch (error) {
      console.error("Error fetching changes:", error);
      toast({
        title: "Erro",
        description: "Erro ao carregar solicitações de mudança",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchUserItems = async () => {
    try {
      const [workoutRes, dietRes] = await Promise.all([
        api.get("treinos/"),
        api.get("dietas/")
      ]);
      const workouts = Array.isArray(workoutRes.data) ? workoutRes.data : [];
      const diets = Array.isArray(dietRes.data) ? dietRes.data : [];
      setWorkouts(workouts.filter((w: Treino) => w.cliente === user?.id));
      setDiets(diets.filter((d: Dieta) => d.cliente === user?.id));
    } catch (error) {
      console.error("Error fetching user items:", error);
    }
  };

  // Combine and format all changes
  const allChanges: ChangeRequest[] = [
    ...exerciseChanges.map(change => ({
      ...change,
      type: 'workout' as const,
      status: 'approved' as const // API doesn't have status field
    })),
    ...mealChanges.map(change => ({
      ...change,
      type: 'diet' as const,
      status: 'approved' as const // API doesn't have status field
    }))
  ];

  const filteredRequests = activeTab === "all" 
    ? allChanges 
    : allChanges.filter(req => req.status === activeTab);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };
  
  const getStatusColor = (status: string) => {
    switch(status) {
      case "pending":
        return "bg-amber-100 text-amber-800";
      case "approved":
        return "bg-green-100 text-green-800";
      case "rejected":
        return "bg-red-100 text-red-800";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!itemToChange || !reason) {
      toast({
        title: "Erro",
        description: "Por favor, preencha todos os campos obrigatórios",
        variant: "destructive",
      });
      return;
    }

    try {
      setSubmitting(true);
      
      const endpoint = changeType === "workout" ? "trocas-exercicios/" : "trocas-refeicoes/";
      const data = {
        cliente: user?.id,
        motivo: reason,
        ...(changeType === "workout" 
          ? { 
              exercicio_antigo: parseInt(itemToChange),
              exercicio_novo: parseInt(itemToChange) // In a real app, you'd select a new exercise
            }
          : { 
              refeicao_antiga: parseInt(itemToChange),
              refeicao_nova: parseInt(itemToChange) // In a real app, you'd select a new meal
            }
        )
      };
      
      await api.post(endpoint, data);
      
      toast({
        title: "Sucesso",
        description: "Solicitação de mudança enviada com sucesso",
      });
      
      // Reset form
      setReason("");
      setSuggestion("");
      setItemToChange("");
      
      // Refresh changes
      fetchChanges();
    } catch (error) {
      console.error("Error submitting change request:", error);
      toast({
        title: "Erro",
        description: "Erro ao enviar solicitação de mudança",
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleApprove = async (changeId: number, type: 'workout' | 'diet') => {
    try {
      const endpoint = type === "workout" 
        ? `trocas-exercicios/${changeId}/aprovar/` 
        : `trocas-refeicoes/${changeId}/aprovar/`;
      
      await api.post(endpoint);
      
      toast({
        title: "Sucesso",
        description: "Solicitação aprovada com sucesso",
      });
      
      fetchChanges();
    } catch (error) {
      console.error("Error approving change:", error);
      toast({
        title: "Erro",
        description: "Erro ao aprovar solicitação",
        variant: "destructive",
      });
    }
  };

  const handleReject = async (changeId: number, type: 'workout' | 'diet') => {
    try {
      const endpoint = type === "workout" 
        ? `trocas-exercicios/${changeId}/rejeitar/` 
        : `trocas-refeicoes/${changeId}/rejeitar/`;
      
      await api.post(endpoint);
      
      toast({
        title: "Sucesso",
        description: "Solicitação rejeitada",
      });
      
      fetchChanges();
    } catch (error) {
      console.error("Error rejecting change:", error);
      toast({
        title: "Erro",
        description: "Erro ao rejeitar solicitação",
        variant: "destructive",
      });
    }
  };
  
  const getTypeIcon = (type: string) => {
    return type === "workout" ? (
      <Dumbbell className="h-5 w-5 text-fitblue-500" />
    ) : (
      <Utensils className="h-5 w-5 text-fitorange-500" />
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-fitblue-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Solicitações de Mudança</h1>
        <p className="text-muted-foreground">
          Solicite mudanças em seus treinos e planos de dieta
        </p>
      </div>
      
      <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3 mb-4">
          <TabsTrigger value="all">Todas as Solicitações</TabsTrigger>
          <TabsTrigger value="pending">Pendentes</TabsTrigger>
          <TabsTrigger value="approved">Resolvidas</TabsTrigger>
        </TabsList>
        
        <TabsContent value={activeTab} className="space-y-4">
          {filteredRequests.length > 0 ? (
            filteredRequests.map(request => (
              <Card key={`${request.type}-${request.id}`} className="overflow-hidden">
                <CardHeader className="flex flex-row items-center justify-between pb-2 gap-2">
                  <div className="flex items-center gap-2">
                    {getTypeIcon(request.type)}
                    <div>
                      <CardTitle className="text-lg">
                        {request.type === 'workout' 
                          ? request.exercicio_antigo?.nome || 'Exercício'
                          : request.refeicao_antiga?.nome || 'Refeição'
                        }
                      </CardTitle>
                      <CardDescription>
                        Solicitado em {formatDate(request.data_troca)}
                      </CardDescription>
                    </div>
                  </div>
                  
                  <Badge className={getStatusColor(request.status || 'approved')}>
                    {request.status === "pending" ? (
                      <span className="flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5" />
                        Pendentes
                      </span>
                    ) : (request.status || 'approved') === "approved" ? (
                      <span className="flex items-center gap-1">
                        <CheckCircle className="h-3.5 w-3.5" />
                        Aprovada
                      </span>
                    ) : (
                      <span className="flex items-center gap-1">
                        <XCircle className="h-3.5 w-3.5" />
                        Rejeitada
                      </span>
                    )}
                  </Badge>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-2">
                    <div>
                      <h4 className="font-medium text-sm">Motivo:</h4>
                      <p className="text-sm text-muted-foreground">{request.motivo}</p>
                    </div>
                    
                    {request.type === 'workout' && request.exercicio_novo && (
                      <div>
                        <h4 className="font-medium text-sm">Novo Exercício:</h4>
                        <p className="text-sm text-muted-foreground">{request.exercicio_novo.nome}</p>
                      </div>
                    )}
                    
                    {request.type === 'diet' && request.refeicao_nova && (
                      <div>
                        <h4 className="font-medium text-sm">Nova Refeição:</h4>
                        <p className="text-sm text-muted-foreground">{request.refeicao_nova.nome}</p>
                      </div>
                    )}
                    
                  </div>
                </CardContent>
                
                <CardFooter className="flex justify-end gap-2">
                  {request.status === "pending" && isProfessional && (
                    <>
                      <Button 
                        variant="outline" 
                        size="sm"
                        className="gap-1 text-green-600 hover:bg-green-50"
                        aria-label="Approve request"
                        onClick={() => handleApprove(request.id, request.type)}
                      >
                        <CheckCircle className="h-4 w-4" />
                        Aprovar
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        className="gap-1 text-red-600 hover:bg-red-50"
                        aria-label="Reject request"
                        onClick={() => handleReject(request.id, request.type)}
                      >
                        <XCircle className="h-4 w-4" />
                        Rejeitar
                      </Button>
                    </>
                  )}
                </CardFooter>
              </Card>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center">
              <RefreshCw className="h-12 w-12 text-muted-foreground/50" />
              <h3 className="mt-4 text-lg font-medium">Nenhuma solicitação de mudança</h3>
              <p className="mb-4 mt-2 text-sm text-muted-foreground">
                {activeTab === "all" ? 
                  "Você ainda não fez nenhuma solicitação de mudança." : 
                  "Você não tem solicitações de mudança pendentes."}
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>
      
      {!isProfessional && (
        <Card>
          <CardHeader>
            <CardTitle>Nova Solicitação de Mudança</CardTitle>
            <CardDescription>
              Solicite uma mudança em seu treino ou plano de dieta
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid gap-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label htmlFor="change-type" className="text-sm font-medium">Tipo</label>
                    <Select value={changeType} onValueChange={setChangeType}>
                      <SelectTrigger id="change-type" aria-label="Select change type">
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="workout">Workout</SelectItem>
                        <SelectItem value="diet">Diet</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <label htmlFor="item-to-change" className="text-sm font-medium">Item</label>
                    <Select value={itemToChange} onValueChange={setItemToChange}>
                      <SelectTrigger id="item-to-change" aria-label="Select item to change">
                        <SelectValue placeholder="Select item" />
                      </SelectTrigger>
                      <SelectContent>
                        {changeType === "workout" ? (
                          workouts.length > 0 ? (
                            workouts.flatMap(workout => 
                              workout.exercicios?.map(ex => (
                                <SelectItem key={ex.id} value={ex.id.toString()}>
                                  {ex.nome} ({workout.nome})
                                </SelectItem>
                              )) || []
                            )
                          ) : (
                            <SelectItem value="" disabled>Nenhum exercício disponível</SelectItem>
                          )
                        ) : (
                          diets.length > 0 ? (
                            diets.flatMap(diet => 
                              diet.refeicoes?.map(meal => (
                                <SelectItem key={meal.id} value={meal.id.toString()}>
                                  {meal.nome} ({diet.nome})
                                </SelectItem>
                              )) || []
                            )
                          ) : (
                            <SelectItem value="" disabled>Nenhuma refeição disponível</SelectItem>
                          )
                        )}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="reason" className="text-sm font-medium">Motivo da mudança</label>
                  <Textarea 
                    id="reason" 
                    placeholder="Por que você precisa desta mudança?" 
                    value={reason} 
                    onChange={(e) => setReason(e.target.value)}
                    aria-label="Reason for requesting change"
                  />
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="suggestion" className="text-sm font-medium">Sua sugestão</label>
                  <Textarea 
                    id="suggestion" 
                    placeholder="Para o que você gostaria de mudar?" 
                    value={suggestion} 
                    onChange={(e) => setSuggestion(e.target.value)}
                    aria-label="Suggestion for the change"
                  />
                </div>
              </div>
              
              <Button 
                type="submit" 
                className="w-full md:w-auto"
                disabled={!reason || !itemToChange || submitting}
                aria-label="Submit change request"
              >
                {submitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Enviando...
                  </>
                ) : (
                  "Enviar Solicitação"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Changes;
