
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Dumbbell, Utensils, Users, RefreshCcw } from "lucide-react";

const Index = () => {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-30 w-full border-b bg-background">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-fitblue-500 text-white font-bold">
              FT
            </div>
            <span className="font-bold text-xl">FitTrack</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-6">
            <Link to="#features" className="text-sm font-medium hover:text-fitblue-500 transition-colors">
              Recursos
            </Link>
            <Link to="#plans" className="text-sm font-medium hover:text-fitblue-500 transition-colors">
              Planos
            </Link>
            <Link to="#testimonials" className="text-sm font-medium hover:text-fitblue-500 transition-colors">
              Depoimentos
            </Link>
          </nav>
          
          <div className="flex items-center gap-2">
            <Link to="/login">
              <Button variant="outline" className="hidden sm:flex">Entrar</Button>
            </Link>
            <Link to="/login">
              <Button>Começar</Button>
            </Link>
          </div>
        </div>
      </header>
      
      {/* Hero section */}
      <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-white to-blue-50">
        <div className="container flex flex-col items-center justify-center gap-4 px-4 text-center md:px-6">
          <div className="space-y-3">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
              Seu Sistema Completo de Gerenciamento Fitness
            </h1>
            <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
              Acompanhe treinos, monitore planos de dieta e alcance seus objetivos fitness com orientação personalizada de treinadores e nutricionistas.
            </p>
          </div>
          <div className="flex flex-col gap-2 min-[400px]:flex-row">
            <Link to="/login">
              <Button size="lg">Começar</Button>
            </Link>
            <Link to="#features">
              <Button variant="outline" size="lg">Saiba Mais</Button>
            </Link>
          </div>
        </div>
      </section>
      
      {/* Features section */}
      <section id="features" className="w-full py-12 md:py-24 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center gap-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter md:text-4xl">Recursos</h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                Tudo que você precisa para gerenciar sua jornada fitness em um só lugar
              </p>
            </div>
          </div>
          
          <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-2 lg:grid-cols-4">
            <div className="flex flex-col items-center space-y-2 rounded-lg border p-6 shadow-sm transition-all hover:shadow-md">
              <Dumbbell className="h-12 w-12 text-fitblue-500" />
              <h3 className="text-xl font-bold">Planos de Treino</h3>
              <p className="text-center text-sm text-muted-foreground">
                Rotinas de exercícios personalizadas criadas por treinadores profissionais
              </p>
            </div>
            <div className="flex flex-col items-center space-y-2 rounded-lg border p-6 shadow-sm transition-all hover:shadow-md">
              <Utensils className="h-12 w-12 text-fitgreen-500" />
              <h3 className="text-xl font-bold">Gerenciamento de Dieta</h3>
              <p className="text-center text-sm text-muted-foreground">
                Planos alimentares desenvolvidos por nutricionistas adaptados aos seus objetivos
              </p>
            </div>
            <div className="flex flex-col items-center space-y-2 rounded-lg border p-6 shadow-sm transition-all hover:shadow-md">
              <Users className="h-12 w-12 text-fitorange-500" />
              <h3 className="text-xl font-bold">Suporte Profissional</h3>
              <p className="text-center text-sm text-muted-foreground">
                Acesso a treinadores e nutricionistas certificados
              </p>
            </div>
            <div className="flex flex-col items-center space-y-2 rounded-lg border p-6 shadow-sm transition-all hover:shadow-md">
              <RefreshCcw className="h-12 w-12 text-fitblue-300" />
              <h3 className="text-xl font-bold">Ajustes de Plano</h3>
              <p className="text-center text-sm text-muted-foreground">
                Solicite mudanças em seus treinos e refeições com base em sua assinatura
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Plans section */}
      <section id="plans" className="w-full py-12 md:py-24 lg:py-32 bg-gray-50">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center gap-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter md:text-4xl">Planos de Assinatura</h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                Escolha o plano que atende suas necessidades
              </p>
            </div>
          </div>
          
          <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-3">
            {/* Basic Plan */}
            <div className="flex flex-col rounded-lg border shadow-sm">
              <div className="p-6">
                <h3 className="text-xl font-bold">Básico</h3>
                <div className="mt-4 text-3xl font-bold">R$29<span className="text-sm font-normal text-muted-foreground">/mês</span></div>
                <ul className="mt-4 space-y-2 text-sm">
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    1 plano de treino
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    1 plano de dieta
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    1 solicitação de mudança por mês
                  </li>
                </ul>
              </div>
              <div className="flex flex-col items-center justify-center gap-4 p-6 bg-gray-50 rounded-b-lg">
                <Link to="/login" className="w-full">
                  <Button variant="outline" className="w-full">Começar</Button>
                </Link>
              </div>
            </div>
            
            {/* Pro Plan */}
            <div className="flex flex-col rounded-lg border border-fitblue-200 shadow-md relative">
              <div className="absolute -top-4 left-0 right-0 mx-auto w-32 rounded-full bg-fitblue-500 py-1 text-center text-xs font-medium text-white">
                Mais Popular
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold">Pro</h3>
                <div className="mt-4 text-3xl font-bold">R$49<span className="text-sm font-normal text-muted-foreground">/mês</span></div>
                <ul className="mt-4 space-y-2 text-sm">
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    3 planos de treino
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    2 planos de dieta
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    5 solicitações de mudança por mês
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Acompanhamento de progresso
                  </li>
                </ul>
              </div>
              <div className="flex flex-col items-center justify-center gap-4 p-6 bg-blue-50 rounded-b-lg">
                <Link to="/login" className="w-full">
                  <Button className="w-full">Começar</Button>
                </Link>
              </div>
            </div>
            
            {/* Premium Plan */}
            <div className="flex flex-col rounded-lg border shadow-sm">
              <div className="p-6">
                <h3 className="text-xl font-bold">Premium</h3>
                <div className="mt-4 text-3xl font-bold">R$79<span className="text-sm font-normal text-muted-foreground">/mês</span></div>
                <ul className="mt-4 space-y-2 text-sm">
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Planos de treino ilimitados
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Planos de dieta ilimitados
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Solicitações de mudança ilimitadas
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Suporte prioritário
                  </li>
                  <li className="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="mr-2 h-4 w-4 text-green-500"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Análises avançadas
                  </li>
                </ul>
              </div>
              <div className="flex flex-col items-center justify-center gap-4 p-6 bg-gray-50 rounded-b-lg">
                <Link to="/login" className="w-full">
                  <Button variant="outline" className="w-full">Começar</Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="w-full border-t py-6 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
          <p className="text-xs text-muted-foreground md:text-sm">
            © 2025 FitTrack. Todos os direitos reservados.
          </p>
          <div className="flex items-center gap-4 text-sm">
            <Link to="#" className="text-muted-foreground underline-offset-4 hover:underline">
              Termos
            </Link>
            <Link to="#" className="text-muted-foreground underline-offset-4 hover:underline">
              Privacidade
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
