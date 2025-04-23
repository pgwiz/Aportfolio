from datetime import date
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.db.models import Avg
from .models import Profile, Skill, Project, Experience, SocialLink, Content, Interactive
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ProjectSerializer,
    ExperienceSerializer,
    SocialLinkSerializer,
    ContentSerializer,
    InteractiveSerializer
)
# profile_app/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Skill, Project, SocialLink
from .serializers import ProfileSerializer, SkillSerializer, ProjectSerializer, SocialLinkSerializer

class HomePageView(TemplateView):
    """
    View for rendering the homepage of the portfolio.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch portfolio data
        try:
            profile = Profile.objects.first()  # Assuming one profile per user
            skills = Skill.objects.all()
            projects = Project.objects.all()
            social_links = SocialLink.objects.all()

            # Serialize data (optional, if needed for JavaScript consumption)
            context['profile'] = ProfileSerializer(profile).data if profile else None
            context['skills'] = SkillSerializer(skills, many=True).data
            context['projects'] = ProjectSerializer(projects, many=True).data
            context['social_links'] = SocialLinkSerializer(social_links, many=True).data
        except Exception as e:
            # Log the error or handle gracefully
            context['error'] = "Failed to load portfolio data."

        return context
        
class IsProfileOwner(permissions.BasePermission):
    """Custom permission to only allow profile owners to edit"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class BaseProfileViewSet(viewsets.ModelViewSet):
    """Base ViewSet with common profile-related functionality"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return self.queryset.filter(profile__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
# profile_app/views.py
from .models import Skill
from .serializers import SkillSerializer

class SkillUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = request.user.profile.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProfileOwner]
    queryset = Profile.objects.select_related('user').prefetch_related(
        'skills', 'projects', 'experiences', 'social_links', 'contents'
    )

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        profile = request.user.profile
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        serializer = self.get_serializer(
            profile, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProjectFilter(filters.FilterSet):
    tech_stack = filters.CharFilter(method='filter_tech_stack')
    
    class Meta:
        model = Project
        fields = ['project_type']
        filter_overrides = {
            'tech_stack': {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'method': 'filter_tech_stack'
                }
            }
        }
    
    def filter_tech_stack(self, queryset, name, value):
        return queryset.filter(tech_stack__contains=value)

class ProjectViewSet(BaseProfileViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProjectFilter

class SkillViewSet(BaseProfileViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

class ExperienceViewSet(BaseProfileViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()

class SocialLinkViewSet(BaseProfileViewSet):
    serializer_class = SocialLinkSerializer
    queryset = SocialLink.objects.all()

class ContentViewSet(BaseProfileViewSet):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

class InteractiveViewSet(viewsets.ModelViewSet):
    serializer_class = InteractiveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch']
    queryset = Interactive.objects.all()

    def get_object(self):
        return self.request.user.profile.interactive

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PortfolioStatsView(APIView):
    def get(self, request):
        profile = request.user.profile
        stats = {
            'projects': profile.projects.count(),
            'skills': profile.skills.count(),
            'avg_skill': profile.skills.aggregate(Avg('proficiency'))['proficiency__avg'],
            'experience_years': (date.today() - profile.experiences.earliest('start_date').start_date).days // 365
        }
        return Response(stats)