from rest_framework.routers import DefaultRouter
from .viewsets import BaseReportViewSet

router = DefaultRouter()

router.register(r'reports', BaseReportViewSet, basename='reports')

urlpatterns = router.urls