
import { useState, useEffect } from "react";
import { Outlet, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { toast } from "@/components/ui/use-toast";

export const DashboardLayout = () => {
  const { isAuthenticated, loading, user, perfil, hasRole, checkTokenExpiration } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const location = useLocation();
  
  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  
  // Check route access based on user role
  useEffect(() => {
    if (!loading && isAuthenticated && user) {
      // Route-specific role requirements
      const routeRoles: Record<string, string[]> = {
        "/workouts": ["admin", "trainer", "client"],
        "/diets": ["admin", "nutritionist", "client"],
        "/changes": ["admin", "nutritionist", "trainer", "client"],
        "/users": ["admin"],
      };
      
      const currentPath = location.pathname;
      const requiredRoles = routeRoles[currentPath];
      
      console.log("Route Guard Debug:", {
        currentPath,
        requiredRoles,
        userRole: perfil?.tipo || (user?.is_staff ? 'admin' : 'unknown'),
        perfilTipo: perfil?.tipo,
        hasAccess: requiredRoles ? hasRole(requiredRoles as any[]) : true,
        user,
        perfil,
      });
      
      // Skip route guard check if perfil is not loaded yet for non-admin users
      if (!user.is_staff && !perfil) {
        console.log("Waiting for perfil to load...");
        return;
      }
      
      if (requiredRoles && !hasRole(requiredRoles as any[])) {
        console.log("Access denied - redirecting to dashboard");
        toast({
          title: "Access denied",
          description: "You don't have permission to access this page",
          variant: "destructive",
        });
        
        // Redirect to dashboard if user doesn't have access
        window.location.href = "/dashboard";
      }
    }
  }, [location.pathname, loading, isAuthenticated, user, perfil, hasRole]);
  
  // Check token expiration on route change
  useEffect(() => {
    if (isAuthenticated) {
      const isTokenValid = checkTokenExpiration();
      if (!isTokenValid) {
        toast({
          title: "Session expired",
          description: "Your session has expired. Please login again.",
          variant: "destructive",
        });
      }
    }
  }, [location.pathname, isAuthenticated, checkTokenExpiration]);
  
  // Close sidebar when clicking outside on mobile
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setIsSidebarOpen(false);
      }
    };
    
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center" role="status" aria-live="polite">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary" aria-label="Loading"></div>
        <span className="sr-only">Loading...</span>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return (
    <div className="min-h-screen bg-background">
      {/* Backdrop for mobile sidebar */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-10 bg-primary/20 backdrop-blur-sm md:hidden"
          onClick={toggleSidebar}
          aria-hidden="true"
        />
      )}
      
      <Sidebar isOpen={isSidebarOpen} />
      
      <div className="flex min-h-screen flex-col md:pl-64">
        <Navbar toggleSidebar={toggleSidebar} />
        
        <main className="flex-1 p-4 md:p-6" tabIndex={-1}>
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
