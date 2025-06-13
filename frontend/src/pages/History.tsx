
import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { format, parseISO } from "date-fns";
import { ptBR } from "date-fns/locale";
import { Calendar as CalendarIcon, Dumbbell, Utensils, Search, Loader2, ChevronLeft, ChevronRight } from "lucide-react";
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import api from "@/lib/api";
import { HistoricoTreino, HistoricoDieta } from "@/types/types";
import { useToast } from "@/components/ui/use-toast";

const History = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState("workouts");
  const [searchQuery, setSearchQuery] = useState("");
  const [dateFilter, setDateFilter] = useState<Date | undefined>(undefined);
  const [typeFilter, setTypeFilter] = useState<string>("all");
  
  // API data states
  const [workoutHistory, setWorkoutHistory] = useState<HistoricoTreino[]>([]);
  const [dietHistory, setDietHistory] = useState<HistoricoDieta[]>([]);
  const [loadingWorkouts, setLoadingWorkouts] = useState(true);
  const [loadingDiets, setLoadingDiets] = useState(true);
  
  // Pagination states
  const [workoutPage, setWorkoutPage] = useState(1);
  const [dietPage, setDietPage] = useState(1);
  const [workoutTotalPages, setWorkoutTotalPages] = useState(1);
  const [dietTotalPages, setDietTotalPages] = useState(1);
  const itemsPerPage = 10;
  
  // Fetch workout history
  useEffect(() => {
    const fetchWorkoutHistory = async () => {
      setLoadingWorkouts(true);
      try {
        console.log('Fetching workout history...');
        const response = await api.get(`historico-treinos/?page=${workoutPage}&page_size=${itemsPerPage}`);
        console.log('Workout history response:', response.data);
        setWorkoutHistory(response.data.results || []);
        setWorkoutTotalPages(Math.ceil((response.data.count || 0) / itemsPerPage));
      } catch (error) {
        console.error('Error fetching workout history:', error);
        toast({
          title: "Erro",
          description: "Erro ao buscar histórico de treinos",
          variant: "destructive",
        });
      } finally {
        setLoadingWorkouts(false);
      }
    };
    
    fetchWorkoutHistory();
  }, [workoutPage, toast]);
  
  // Fetch diet history
  useEffect(() => {
    const fetchDietHistory = async () => {
      setLoadingDiets(true);
      try {
        console.log('Fetching diet history...');
        const response = await api.get(`historico-dietas/?page=${dietPage}&page_size=${itemsPerPage}`);
        console.log('Diet history response:', response.data);
        setDietHistory(response.data.results || []);
        setDietTotalPages(Math.ceil((response.data.count || 0) / itemsPerPage));
      } catch (error) {
        console.error('Error fetching diet history:', error);
        toast({
          title: "Erro",
          description: "Erro ao buscar histórico de dietas",
          variant: "destructive",
        });
      } finally {
        setLoadingDiets(false);
      }
    };
    
    fetchDietHistory();
  }, [dietPage, toast]);
  
  // Format date for display
  const formatDate = (dateString: string) => {
    try {
      if (!dateString) return 'Data não disponível';
      const date = parseISO(dateString);
      if (isNaN(date.getTime())) return dateString;
      return format(date, "dd 'de' MMMM 'de' yyyy", { locale: ptBR });
    } catch (error) {
      console.error('Error formatting date:', error, dateString);
      return dateString || 'Data inválida';
    }
  };
  
  // Filter workouts based on search query, date and type
  const filteredWorkouts = workoutHistory.filter(history => {
    try {
      // Search filter
      const searchLower = searchQuery.toLowerCase();
      const matchesSearch = !searchQuery || 
        (history.treino?.nome?.toLowerCase().includes(searchLower)) || 
        (history.treino?.descricao?.toLowerCase().includes(searchLower)) ||
        (history.observacoes?.toLowerCase().includes(searchLower));
      
      // Date filter
      const matchesDate = !dateFilter || (() => {
        try {
          const historyDate = parseISO(history.data_inicio);
          return format(historyDate, "yyyy-MM-dd") === format(dateFilter, "yyyy-MM-dd");
        } catch {
          return false;
        }
      })();
      
      return matchesSearch && matchesDate;
    } catch (error) {
      console.error('Error filtering workout:', error, history);
      return false;
    }
  });
  
  // Filter diets based on search query and date
  const filteredDiets = dietHistory.filter(history => {
    try {
      // Search filter
      const searchLower = searchQuery.toLowerCase();
      const matchesSearch = !searchQuery || 
        (history.dieta?.nome?.toLowerCase().includes(searchLower)) || 
        (history.dieta?.descricao?.toLowerCase().includes(searchLower)) ||
        (history.observacoes?.toLowerCase().includes(searchLower));
      
      // Date filter
      const matchesDate = !dateFilter || (() => {
        try {
          const historyDate = parseISO(history.data_inicio);
          return format(historyDate, "yyyy-MM-dd") === format(dateFilter, "yyyy-MM-dd");
        } catch {
          return false;
        }
      })();
      
      return matchesSearch && matchesDate;
    } catch (error) {
      console.error('Error filtering diet:', error, history);
      return false;
    }
  });

  const renderWorkoutHistory = () => {
    if (loadingWorkouts) {
      return (
        <div className="flex flex-col items-center justify-center p-8">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          <p className="mt-2 text-muted-foreground">Carregando histórico de treinos...</p>
        </div>
      );
    }
    
    if (workoutHistory.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center p-8 text-muted-foreground">
          <Dumbbell className="h-12 w-12 mb-4 opacity-30" />
          <p>Nenhum histórico de treino encontrado.</p>
        </div>
      );
    }
    
    if (filteredWorkouts.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center p-8 text-muted-foreground">
          <Dumbbell className="h-12 w-12 mb-4 opacity-30" />
          <p>Nenhum histórico de treino encontrado.</p>
          <p className="text-sm">Tente ajustar seus filtros.</p>
        </div>
      );
    }
    
    return (
      <>
        <div className="space-y-4">
          {filteredWorkouts.map((history) => (
            <Card key={history.id}>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-xl">{history.treino?.nome || 'Treino sem nome'}</CardTitle>
                  <div className="flex flex-col items-end">
                    <span className="text-sm text-muted-foreground">
                      Início: {formatDate(history.data_inicio)}
                    </span>
                    {history.data_fim && (
                      <span className="text-sm text-muted-foreground">
                        Fim: {formatDate(history.data_fim)}
                      </span>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">{history.treino?.descricao || 'Sem descrição'}</p>
                  
                  <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm">
                    <span className="flex items-center gap-1">
                      <Dumbbell className="h-4 w-4" />
                      {history.treino?.exercicios?.length || 0} exercícios
                    </span>
                    <span>Duração: {history.treino?.duracao || 0} min</span>
                  </div>
                  
                  {history.treino?.exercicios && history.treino.exercicios.length > 0 && (
                    <div className="mt-2">
                      <h4 className="font-medium text-sm">Exercícios:</h4>
                      <ul className="text-sm text-muted-foreground ml-4">
                        {history.treino.exercicios.slice(0, 3).map((exercise) => (
                          <li key={exercise.id}>{exercise.nome}</li>
                        ))}
                        {history.treino.exercicios.length > 3 && (
                          <li>+ {history.treino.exercicios.length - 3} mais</li>
                        )}
                      </ul>
                    </div>
                  )}
                  
                  {history.observacoes && (
                    <div className="mt-2">
                      <h4 className="font-medium text-sm">Observações:</h4>
                      <p className="text-sm text-muted-foreground">{history.observacoes}</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {/* Pagination */}
        {workoutTotalPages > 1 && (
          <div className="flex items-center justify-center gap-2 mt-6">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setWorkoutPage(p => Math.max(1, p - 1))}
              disabled={workoutPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm">
              Página {workoutPage} de {workoutTotalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setWorkoutPage(p => Math.min(workoutTotalPages, p + 1))}
              disabled={workoutPage === workoutTotalPages}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </>
    );
  };
  
  const renderDietHistory = () => {
    if (loadingDiets) {
      return (
        <div className="flex flex-col items-center justify-center p-8">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          <p className="mt-2 text-muted-foreground">Carregando histórico de dietas...</p>
        </div>
      );
    }
    
    if (dietHistory.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center p-8 text-muted-foreground">
          <Utensils className="h-12 w-12 mb-4 opacity-30" />
          <p>Nenhum histórico de dieta encontrado.</p>
        </div>
      );
    }
    
    if (filteredDiets.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center p-8 text-muted-foreground">
          <Utensils className="h-12 w-12 mb-4 opacity-30" />
          <p>Nenhum histórico de dieta encontrado.</p>
          <p className="text-sm">Tente ajustar seus filtros.</p>
        </div>
      );
    }
    
    return (
      <>
        <div className="space-y-4">
          {filteredDiets.map((history) => (
            <Card key={history.id}>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-xl">{history.dieta?.nome || 'Dieta sem nome'}</CardTitle>
                  <div className="flex flex-col items-end">
                    <span className="text-sm text-muted-foreground">
                      Início: {formatDate(history.data_inicio)}
                    </span>
                    {history.data_fim && (
                      <span className="text-sm text-muted-foreground">
                        Fim: {formatDate(history.data_fim)}
                      </span>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">{history.dieta?.descricao || 'Sem descrição'}</p>
                  
                  <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm">
                    <span>{history.dieta?.refeicoes?.length || 0} refeições</span>
                    <span>{history.dieta?.calorias || 0} calorias totais</span>
                  </div>
                  
                  {history.dieta?.refeicoes && history.dieta.refeicoes.length > 0 && (
                    <div className="mt-2">
                      <h4 className="font-medium text-sm">Refeições:</h4>
                      <ul className="text-sm text-muted-foreground ml-4">
                        {history.dieta.refeicoes.map((meal) => (
                          <li key={meal.id}>
                            {meal.nome} ({meal.calorias} kcal)
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {history.observacoes && (
                    <div className="mt-2">
                      <h4 className="font-medium text-sm">Observações:</h4>
                      <p className="text-sm text-muted-foreground">{history.observacoes}</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {/* Pagination */}
        {dietTotalPages > 1 && (
          <div className="flex items-center justify-center gap-2 mt-6">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setDietPage(p => Math.max(1, p - 1))}
              disabled={dietPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm">
              Página {dietPage} de {dietTotalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setDietPage(p => Math.min(dietTotalPages, p + 1))}
              disabled={dietPage === dietTotalPages}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Histórico de Atividades</h1>
        <p className="text-muted-foreground">
          Acompanhe seus treinos e planos de dieta anteriores
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar histórico..."
            className="pl-8"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <Popover>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              className="w-full sm:w-[220px] justify-start text-left font-normal"
            >
              <CalendarIcon className="mr-2 h-4 w-4" />
              {dateFilter ? (() => {
                try {
                  return format(dateFilter, "PPP", { locale: ptBR });
                } catch {
                  return dateFilter.toLocaleDateString('pt-BR');
                }
              })() : "Filtrar por data"}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0">
            <Calendar
              mode="single"
              selected={dateFilter}
              onSelect={setDateFilter}
              initialFocus
            />
            {dateFilter && (
              <div className="p-3 border-t border-border">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setDateFilter(undefined)}
                  className="w-full"
                >
                  Limpar data
                </Button>
              </div>
            )}
          </PopoverContent>
        </Popover>
        
        {dateFilter && (
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setDateFilter(undefined)}
            className="px-2"
          >
            Limpar filtros
          </Button>
        )}
      </div>

      <Tabs 
        defaultValue="workouts" 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="space-y-4"
      >
        <TabsList>
          <TabsTrigger value="workouts" className="flex items-center gap-2">
            <Dumbbell className="h-4 w-4" />
            <span>Treinos</span>
          </TabsTrigger>
          <TabsTrigger value="diets" className="flex items-center gap-2">
            <Utensils className="h-4 w-4" />
            <span>Dietas</span>
          </TabsTrigger>
        </TabsList>
        <TabsContent value="workouts" className="space-y-4">
          {renderWorkoutHistory()}
        </TabsContent>
        <TabsContent value="diets" className="space-y-4">
          {renderDietHistory()}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default History;
