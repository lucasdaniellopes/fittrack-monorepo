
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dumbbell, Clock, BarChart, ArrowRight, Edit, Trash, Tag } from "lucide-react";
import { Treino } from "@/types/types";
import { cn } from "@/lib/utils";
import { useAuth } from "@/contexts/AuthContext";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";

interface WorkoutCardProps {
  workout: Treino | null | undefined;
  className?: string;
  isLoading?: boolean;
  onViewDetails?: (workout: Treino) => void;
}

// Helper function to determine workout type icon
const getWorkoutTypeIcon = (nome: string) => {
  const nameLower = nome.toLowerCase();
  if (nameLower.includes('força') || nameLower.includes('strength') || nameLower.includes('superior') || nameLower.includes('inferior')) {
    return <Dumbbell className="h-5 w-5" />;
  } else if (nameLower.includes('core') || nameLower.includes('condicionamento')) {
    return <BarChart className="h-5 w-5" />;
  } else {
    return <Clock className="h-5 w-5" />;
  }
};

// Helper function to get workout type tooltip text
const getWorkoutTypeText = (nome: string) => {
  const nameLower = nome.toLowerCase();
  if (nameLower.includes('força') || nameLower.includes('strength') || nameLower.includes('superior') || nameLower.includes('inferior')) {
    return "Treino de Força";
  } else if (nameLower.includes('core') || nameLower.includes('condicionamento')) {
    return "Condicionamento";
  } else {
    return "Cardio/Resistência";
  }
};

// Helper to extract tags from workout name and description
const extractTags = (workout: Treino) => {
  const tags: string[] = [];
  const nameLower = workout.nome.toLowerCase();
  const descLower = workout.descricao?.toLowerCase() || '';
  
  // Common workout tags
  const possibleTags = ['full body', 'upper body', 'lower body', 'core', 'hiit', 'cardio', 'strength'];
  
  possibleTags.forEach(tag => {
    if (nameLower.includes(tag) || descLower.includes(tag)) {
      tags.push(tag);
    }
  });
  
  // Add duration as a tag if exists
  if (workout.duracao) {
    tags.push(`${workout.duracao} min`);
  }
  
  // Return unique tags (no duplicates)
  return [...new Set(tags)];
};

export const WorkoutCardSkeleton = () => (
  <Card className="overflow-hidden border-l-4 border-l-fitblue-500">
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <div className="flex items-center gap-2">
        <Skeleton className="h-8 w-8 rounded-full" />
        <Skeleton className="h-6 w-40" />
      </div>
      <Skeleton className="h-6 w-24" />
    </CardHeader>
    
    <CardContent>
      <Skeleton className="h-4 w-full mb-4" />
      <div className="space-y-2">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-12 w-full" />
        ))}
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-2">
        <Skeleton className="h-4 w-20" />
        <Skeleton className="h-4 w-28 ml-auto" />
      </div>
    </CardContent>
    
    <CardFooter className="pt-0 pb-4 flex justify-end gap-2">
      <Skeleton className="h-9 w-32" />
    </CardFooter>
  </Card>
);

// Get the workout difficulty level based on exercises count
const getWorkoutDifficulty = (workout: Treino) => {
  if (!workout.exercicios || workout.exercicios.length === 0) return "Básico";
  if (workout.exercicios.length <= 4) return "Iniciante";
  if (workout.exercicios.length <= 6) return "Intermediário";
  return "Avançado";
};

export const WorkoutCard = ({ workout, className, isLoading, onViewDetails }: WorkoutCardProps) => {
  const { hasRole, checkTokenExpiration } = useAuth();
  const [isTokenValid, setIsTokenValid] = useState(true);
  
  useEffect(() => {
    setIsTokenValid(checkTokenExpiration());
  }, [checkTokenExpiration]);
  
  const isTrainerOrAdmin = hasRole(["admin", "trainer"]) && isTokenValid;
  
  if (isLoading) {
    return <WorkoutCardSkeleton />;
  }
  
  // Handle null/undefined workout gracefully
  if (!workout) {
    return (
      <Card className={cn("overflow-hidden border-l-4 border-l-gray-300", className)}>
        <CardContent className="text-center py-8">
          <p className="text-muted-foreground">Nenhum treino disponível</p>
        </CardContent>
      </Card>
    );
  }
  
  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return "Data não disponível";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("pt-BR", {
      month: "short",
      day: "numeric",
      year: "numeric",
    }).format(date);
  };

  const workoutTypeIcon = getWorkoutTypeIcon(workout.nome);
  const workoutTypeText = getWorkoutTypeText(workout.nome);
  const tags = extractTags(workout);

  return (
    <Card 
      className={cn("card-hover overflow-hidden border-l-4 border-l-fitblue-500", className)}
      tabIndex={0}
      aria-label={`${workout.nome} treino, ${getWorkoutDifficulty(workout)} dificuldade`}
    >
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center gap-2">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="rounded-full bg-fitblue-100 p-1.5 text-fitblue-500 cursor-help">
                  {workoutTypeIcon}
                </div>
              </TooltipTrigger>
              <TooltipContent>
                <p>{workoutTypeText}</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
          <CardTitle className="text-lg font-bold">{workout.nome}</CardTitle>
        </div>
        <div className="flex items-center space-x-1 rounded-md bg-fitblue-100 px-2 py-0.5 text-xs font-medium text-fitblue-700">
          {getWorkoutDifficulty(workout)}
        </div>
      </CardHeader>
      
      <CardContent>
        {workout.descricao && (
          <p className="text-sm text-muted-foreground mb-4">{workout.descricao}</p>
        )}
        
        {/* Tags row */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3" aria-label="Workout tags">
            {tags.map((tag, index) => (
              <div key={index} className="inline-flex items-center gap-1 bg-muted px-2 py-0.5 rounded-full text-xs">
                <Tag className="h-3 w-3" aria-hidden="true" />
                <span>{tag}</span>
              </div>
            ))}
          </div>
        )}
        
        <div className="space-y-2">
          {workout.exercicios && workout.exercicios.length > 0 ? (
            <>
              {workout.exercicios.slice(0, 3).map((exercicio) => (
                <div
                  key={exercicio.id}
                  className="flex items-center justify-between rounded-md bg-muted p-2"
                >
                  <div className="font-medium">{exercicio.nome}</div>
                  {exercicio.descricao && (
                    <div className="text-sm text-muted-foreground">
                      {exercicio.descricao}
                    </div>
                  )}
                </div>
              ))}
              {workout.exercicios.length > 3 && (
                <div className="text-sm text-center text-muted-foreground mt-2">
                  +{workout.exercicios.length - 3} mais exercícios
                </div>
              )}
            </>
          ) : (
            <div className="text-sm text-center text-muted-foreground py-2">
              Nenhum exercício cadastrado
            </div>
          )}
        </div>
        
        <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
          <div className="flex items-center gap-1 text-muted-foreground">
            <Clock className="h-3.5 w-3.5" aria-hidden="true" /> 
            <span>{workout.duracao ? `${workout.duracao} min` : 'Duração não definida'}</span>
          </div>
          <div className="flex items-center gap-1 text-muted-foreground text-right justify-end">
            <span>{workout.exercicios ? `${workout.exercicios.length} exercícios` : '0 exercícios'}</span>
          </div>
        </div>
      </CardContent>
      
      <CardFooter className="pt-0 pb-4 flex justify-end gap-2 flex-wrap">
        <Button 
          variant="ghost" 
          size="sm" 
          className="gap-1"
          onClick={() => onViewDetails && onViewDetails(workout)}
          aria-label={`Ver detalhes de ${workout.nome}`}
        >
          Ver Detalhes <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </Button>
        
        {isTrainerOrAdmin ? (
          <>
            <Button 
              variant="outline" 
              size="sm" 
              className="gap-1"
              aria-label={`Editar ${workout.nome}`}
            >
              <Edit className="h-4 w-4" aria-hidden="true" /> Editar
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="gap-1 text-destructive hover:bg-destructive/10"
              aria-label={`Excluir ${workout.nome}`}
            >
              <Trash className="h-4 w-4" aria-hidden="true" /> Excluir
            </Button>
          </>
        ) : (
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-1 text-fitorange-600 hover:bg-fitorange-50"
            aria-label={`Solicitar mudança para ${workout.nome}`}
          >
            Solicitar Mudança
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

export default WorkoutCard;
