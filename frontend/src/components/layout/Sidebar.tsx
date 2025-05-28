
import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, Dumbbell, Utensils, RefreshCcw, History, Settings, Users } from "lucide-react";
import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuth } from "@/contexts/AuthContext";

interface SidebarProps {
  isOpen: boolean;
}

export const Sidebar = ({ isOpen }: SidebarProps) => {
  const location = useLocation();
  const { user, perfil, hasRole } = useAuth();
  const [forceUpdate, setForceUpdate] = React.useState(0);
  
  // Debug effect and force update when perfil changes
  React.useEffect(() => {
    console.log("Sidebar Debug - User/Perfil Update:", {
      user: user?.username,
      userRole: user?.role,
      perfil,
      perfilTipo: perfil?.tipo,
    });
    // Force re-render when perfil changes
    if (perfil) {
      setForceUpdate(prev => prev + 1);
    }
  }, [user, perfil]);
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };
  
  const navItems = [
    {
      title: "Painel",
      icon: Home,
      href: "/dashboard",
      roles: ["admin", "nutritionist", "trainer", "client"],
    },
    {
      title: "Treinos",
      icon: Dumbbell,
      href: "/workouts",
      roles: ["admin", "trainer", "client"],
    },
    {
      title: "Dietas",
      icon: Utensils,
      href: "/diets",
      roles: ["admin", "nutritionist", "client"],
    },
    {
      title: "Solicitações de Troca",
      icon: RefreshCcw,
      href: "/changes",
      roles: ["admin", "nutritionist", "trainer", "client"],
    },
    {
      title: "Histórico",
      icon: History,
      href: "/history",
      roles: ["admin", "nutritionist", "trainer", "client"],
    },
    {
      title: "Usuários",
      icon: Users,
      href: "/users",
      roles: ["admin"],
    },
    {
      title: "Configurações",
      icon: Settings,
      href: "/settings",
      roles: ["admin", "nutritionist", "trainer", "client"],
    },
  ];
  
  // Filter items based on user role
  const filteredNavItems = navItems.filter((item) => {
    if (!user) return false;
    
    // Temporário: mostrar todos os itens exceto Usuários (apenas admin)
    if (item.title === "Usuários" && !user.is_staff) {
      return false;
    }
    
    // Mostrar todos os outros itens para todos os usuários logados
    return true;
  });
  
  console.log("SIDEBAR - Final filtered items:", {
    count: filteredNavItems.length,
    items: filteredNavItems.map(item => item.title),
    perfil: perfil?.tipo,
    user: user?.username
  });
  
  console.log("Filtered nav items:", filteredNavItems.map(item => item.title));

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-20 flex w-64 flex-col bg-card border-r border-border transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}
    >
      <div className="flex h-16 items-center border-b border-border px-6">
        <Link to="/dashboard" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground font-bold text-lg">
            FT
          </div>
          <span className="font-bold text-xl text-card-foreground">FitTrack</span>
        </Link>
      </div>
      
      <ScrollArea className="flex-1 overflow-auto py-2">
        <nav className="grid gap-1 px-2">
          {filteredNavItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                "group flex h-10 w-full items-center rounded-md px-3 py-2 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors",
                isActive(item.href) && "bg-muted text-foreground"
              )}
            >
              <item.icon className="mr-2 h-5 w-5" />
              <span>{item.title}</span>
            </Link>
          ))}
        </nav>
      </ScrollArea>
      
      <div className="border-t border-border p-4">
        <div className="text-xs text-muted-foreground">
          {user?.role && (
            <div className="capitalize bg-muted text-muted-foreground rounded-full px-3 py-1 inline-block">
              Perfil: {user.role}
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
