from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Import app viewsets
from authentication.views import PortfolioUserViewSet
from profile_app.views import ProfileViewSet, SkillViewSet, ProjectViewSet
from chat.views import MessageViewSet, NotificationViewSet

# Create a default router for API endpoints
router = routers.DefaultRouter()
router.register(r'auth/users', PortfolioUserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Authentication app endpoints
    path('api/auth/', include('authentication.urls')),
    
    # Profile app endpoints
    path('api/portfolio/', include(router.urls)),
    path('', include('profile_app.urls')),
    path('', include('authentication.urls')),
    path('', include('chat.urls')),
    path('api/portfolio/', include('profile_app.urls')),
    
    # Chat app endpoints
    path('api/chat/', include('chat.urls')),
    
    # WebSocket chat routing (for Django Channels)
   # path('ws/chat/', include('chat.routing.websocket_urls')),
]