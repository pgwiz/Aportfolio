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

# portfolio_project/urls.py
from django.urls import path
from .views import (
    UpdateHeaderView,
    UpdateSkillsView,
    UpdateProjectsView,
    UpdateContactView,
    PortfolioUpdaterView,
    
)

# Non-API routes
non_api_urlpatterns = [
     path('port-update/', PortfolioUpdaterView.as_view(), name='portfolio_updater'),
    path('update-header/', UpdateHeaderView.as_view(), name='update_header'),
    path('update-skills/', UpdateSkillsView.as_view(), name='update_skills'),
    path('update-projects/', UpdateProjectsView.as_view(), name='update_projects'),
    path('update-contact/', UpdateContactView.as_view(), name='update_contact'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('skills/update/', SkillUpdateView.as_view(), name='skills-update'),
    path('', HomePageView.as_view(), name='home'),
]

# API routes
api_urlpatterns = [
    path('api/profile/', include(router.urls)),
    path('api/skills/', include(router.urls)),
    path('api/portfolio/', include(router.urls)),
    path('api/portfolio/stats/', views.PortfolioStatsView.as_view()),
]

# Combine all routes
urlpatterns = non_api_urlpatterns + api_urlpatterns