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
    UpdateExperienceView,
    UpdateSocialLinksView,
    UpdateContentView,
    UpdateInteractiveView,

    ExperienceAPIView,
    SocialLinksAPIView,
    ContentAPIView,
    InteractiveAPIView,
    
)

# Non-API routes
non_api_urlpatterns = [
     path('port-update/', PortfolioUpdaterView.as_view(), name='portfolio_updater'),
    path('update-header/', UpdateHeaderView.as_view(), name='update_header'),
    path('update-skills/', UpdateSkillsView.as_view(), name='update_skills'),
    path('update-projects/', UpdateProjectsView.as_view(), name='update_projects'),
    
    path('update-experience/', UpdateExperienceView.as_view(), name='update_experience'),
    path('update-social-links/', UpdateSocialLinksView.as_view(), name='update_social_links'),
    path('update-content/', UpdateContentView.as_view(), name='update_content'),
    path('update-interactive/', UpdateInteractiveView.as_view(), name='update_interactive'),

    path('api/experience/', ExperienceAPIView.as_view(), name='experience_api'),
    path('api/social-links/', SocialLinksAPIView.as_view(), name='social_links_api'),
    path('api/content/', ContentAPIView.as_view(), name='content_api'),
    path('api/interactive/', InteractiveAPIView.as_view(), name='interactive_api'),

    #path('contact/', views.ContactView.as_view(), name='contact'),
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