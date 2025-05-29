from rest_framework.routers import DefaultRouter
from .viewsets import BaseNotificationViewSet

router = DefaultRouter()

router.register(r'notifications', BaseNotificationViewSet, basename='notifications')

urlpatterns = router.urls