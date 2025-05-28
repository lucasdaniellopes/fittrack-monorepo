
import { useState, useEffect } from "react";
import { Dumbbell, Utensils, RefreshCcw, Trophy } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatCard } from "@/components/ui/StatCard";
import { WorkoutCard } from "@/components/ui/WorkoutCard";
import { DietCard } from "@/components/ui/DietCard";
import { useAuth } from "@/contexts/AuthContext";
import { Treino, Dieta } from "@/types/types";
import api from "@/lib/api";
import { toast } from "@/hooks/use-toast";
import { Skeleton } from "@/components/ui/skeleton";

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [workoutsCount, setWorkoutsCount] = useState(0);
  const [dietsCount, setDietsCount] = useState(0);
  const [pendingChanges, setPendingChanges] = useState(0);
  const [latestWorkout, setLatestWorkout] = useState<Treino | null>(null);
  const [currentDiet, setCurrentDiet] = useState<Dieta | null>(null);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch all data in parallel
        const [
          workoutsResponse,
          dietsResponse,
          exerciseChangesResponse,
          mealChangesResponse,
          workoutHistoryResponse
        ] = await Promise.all([
          api.get("treinos/"),
          api.get("dietas/"),
          api.get("trocas-exercicios/"),
          api.get("trocas-refeicoes/"),
          api.get("historico-treinos/")
        ]);
        
        // Set workouts count
        const workouts = Array.isArray(workoutsResponse.data) ? workoutsResponse.data : [];
        setWorkoutsCount(workouts.length);
        
        // Set diets count
        const diets = Array.isArray(dietsResponse.data) ? dietsResponse.data : [];
        setDietsCount(diets.length);
        
        // Calculate pending changes (filter by status if needed)
        const exerciseChanges = Array.isArray(exerciseChangesResponse.data) ? exerciseChangesResponse.data : [];
        const mealChanges = Array.isArray(mealChangesResponse.data) ? mealChangesResponse.data : [];
        
        const pendingExerciseChanges = exerciseChanges.filter(
          (change: any) => change.status === "PENDENTE"
        ).length;
        const pendingMealChanges = mealChanges.filter(
          (change: any) => change.status === "PENDENTE"
        ).length;
        setPendingChanges(pendingExerciseChanges + pendingMealChanges);
        
        // Get latest workout from history
        const workoutHistory = Array.isArray(workoutHistoryResponse.data) ? workoutHistoryResponse.data : [];
        if (workoutHistory.length > 0) {
          const latestHistory = workoutHistory[0];
          // If the API returns the full workout object
          if (latestHistory.treino) {
            setLatestWorkout(latestHistory.treino);
          }
        }
        
        // Get current diet (assuming the first one is the current)
        if (diets.length > 0) {
          setCurrentDiet(diets[0]);
        }
        
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        toast({
          title: "Erro ao carregar dados",
          description: "Não foi possível carregar os dados do dashboard. Tente novamente mais tarde.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Bem-vindo, {user?.first_name || user?.username}!</h1>
        <p className="text-muted-foreground">
          Aqui está uma visão geral da sua jornada fitness.
        </p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {loading ? (
          <>
            <Skeleton className="h-32" />
            <Skeleton className="h-32" />
            <Skeleton className="h-32" />
            <Skeleton className="h-32" />
          </>
        ) : (
          <>
            <StatCard
              title="Treinos Ativos"
              value={(workoutsCount || 0).toString()}
              description="Planos de treino atuais"
              icon={<Dumbbell className="h-4 w-4" />}
            />
            <StatCard
              title="Dietas Ativas"
              value={(dietsCount || 0).toString()}
              description="Planos de dieta atuais"
              icon={<Utensils className="h-4 w-4" />}
            />
            <StatCard
              title="Solicitações de Troca"
              value={(pendingChanges || 0).toString()}
              description="Aprovações pendentes"
              icon={<RefreshCcw className="h-4 w-4" />}
            />
            <StatCard
              title="Sequência"
              value="14 dias"
              description="Sequência de consistência atual"
              icon={<Trophy className="h-4 w-4" />}
              trend={{
                value: 27,
                isPositive: true,
              }}
            />
          </>
        )}
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Último Treino</h2>
          {loading ? (
            <Skeleton className="h-64" />
          ) : (
            <WorkoutCard workout={latestWorkout} />
          )}
        </div>
        
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Dieta Atual</h2>
          {loading ? (
            <Skeleton className="h-64" />
          ) : (
            <DietCard diet={currentDiet} />
          )}
        </div>
      </div>
      
      <div>
        <Card>
          <CardHeader>
            <CardTitle>Resumo do Progresso</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center p-8 text-muted-foreground">
              <p>Os gráficos de progresso serão exibidos aqui</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
