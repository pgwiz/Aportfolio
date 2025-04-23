# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# profile_app/urls.py
from django.urls import path
from .views import HomePageView

# profile_app/urls.py
from django.urls import path
from .views import ProfileUpdateView, SkillUpdateView


    
router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'experiences', views.ExperienceViewSet)
router.register(r'social', views.SocialLinkViewSet)
router.register(r'content', views.ContentViewSet)
router.register(r'interactive', views.InteractiveViewSet)

urlpatterns = [
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('skills/update/', SkillUpdateView.as_view(), name='skills-update'),
    path('api/profile/', include(router.urls)),
    path('api/skills/', include(router.urls)),


    path('api/portfolio/', include(router.urls)),
    path('api/portfolio/stats/', views.PortfolioStatsView.as_view()),
    path('', HomePageView.as_view(), name='home'),
]