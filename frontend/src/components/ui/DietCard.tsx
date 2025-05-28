
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Utensils } from "lucide-react";
import { Dieta } from "@/types/types";
import { cn } from "@/lib/utils";

interface DietCardProps {
  diet: Dieta | null | undefined;
  className?: string;
}

export const DietCard = ({ diet, className }: DietCardProps) => {
  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return "Data não disponível";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("pt-BR", {
      month: "short",
      day: "numeric",
      year: "numeric",
    }).format(date);
  };

  // Handle null/undefined diet
  if (!diet) {
    return (
      <Card className={cn("card-hover", className)}>
        <CardContent className="p-6">
          <p className="text-center text-muted-foreground">Nenhuma dieta disponível</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn("card-hover", className)}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-bold">{diet.nome}</CardTitle>
        <Utensils className="h-5 w-5 text-fitgreen-500" />
      </CardHeader>
      <CardContent>
        {diet.descricao && (
          <p className="text-sm text-muted-foreground mb-4">{diet.descricao}</p>
        )}
        <div className="space-y-2">
          {diet.refeicoes && diet.refeicoes.length > 0 ? (
            <>
              {diet.refeicoes.slice(0, 3).map((refeicao) => (
                <div
                  key={refeicao.id}
                  className="flex items-center justify-between rounded-md bg-muted p-2"
                >
                  <div className="font-medium">{refeicao.nome}</div>
                  <div className="text-sm text-muted-foreground">{refeicao.calorias} cal</div>
                </div>
              ))}
              {diet.refeicoes.length > 3 && (
                <div className="text-sm text-center text-muted-foreground mt-2">
                  +{diet.refeicoes.length - 3} mais refeições
                </div>
              )}
            </>
          ) : (
            <div className="text-sm text-center text-muted-foreground p-4">
              Nenhuma refeição cadastrada
            </div>
          )}
        </div>
        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm font-medium">
            Calorias totais: <span className="font-bold">{diet.calorias || 0}</span>
          </div>
          {diet.refeicoes && (
            <div className="text-xs text-muted-foreground">
              {diet.refeicoes.length} refeições
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default DietCard;
