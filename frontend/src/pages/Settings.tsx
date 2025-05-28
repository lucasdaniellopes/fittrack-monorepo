import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Settings as SettingsIcon } from "lucide-react";

const Settings = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Configurações</h1>
        <p className="text-muted-foreground">Gerencie as configurações do sistema</p>
      </div>

      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <SettingsIcon className="h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">Configurações em desenvolvimento</h3>
          <p className="text-muted-foreground text-center">
            Esta página está sendo desenvolvida. Em breve você poderá gerenciar as configurações do sistema aqui.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Settings;