from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="FitTrack API",
      default_version='v1',
      description="API para acompanhamento de treinos e dietas",
      contact=openapi.Contact(email="contact@fittrack.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', RedirectView.as_view(url='/api/docs/', permanent=True)),
    path('docs/', RedirectView.as_view(url='/api/docs/', permanent=True)),
    path('redoc/', RedirectView.as_view(url='/api/redoc/', permanent=True)),
    
    # Authentication
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('accounts.api.v1.routers')),
    
    # Main API - all endpoints consolidated
    path('api/v1/', include('core.api.v1.routers')),
    
    # Root redirect
    path('', RedirectView.as_view(url='/api/v1/', permanent=True), name='index'),
]