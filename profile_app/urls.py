# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# profile_app/urls.py
from django.urls import path
from .views import HomePageView


router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'experiences', views.ExperienceViewSet)
router.register(r'social', views.SocialLinkViewSet)
router.register(r'content', views.ContentViewSet)
router.register(r'interactive', views.InteractiveViewSet)

urlpatterns = [
    path('api/portfolio/', include(router.urls)),
    path('api/portfolio/stats/', views.PortfolioStatsView.as_view()),
    path('', HomePageView.as_view(), name='home'),
]