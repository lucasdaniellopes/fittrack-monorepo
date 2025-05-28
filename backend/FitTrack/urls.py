"""
URL configuration for FitTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.api.v1.routers import router as api_v1_router
from core.api.v1.views import register_user
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="FitTrack API",
        default_version='v1',
        description="API para acompanhamento de treinos e dietas",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_router.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Redirecionamento de caminhos alternativos
    path('swagger/', RedirectView.as_view(url='/api/docs/', permanent=True)),
    path('docs/', RedirectView.as_view(url='/api/docs/', permanent=True)),
    path('redoc/', RedirectView.as_view(url='/api/redoc/', permanent=True)),
    path('api/v1/auth/register/', register_user, name='register_user'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Redirecionamento da raiz para api/v1/
    path('', RedirectView.as_view(url='/api/v1/', permanent=True), name='index'),
]