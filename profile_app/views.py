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


# portfolio/views.py
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Profile, Skill, Project
from .serializers import ProfileSerializer, SkillSerializer, ProjectSerializer

PortfolioUser = get_user_model()

class PortfolioUpdaterView(LoginRequiredMixin, View):
    """
    Renders the portfolio updater page with collapsible sections.
    """
    template_name = 'portfolio-updater.html'

    def get(self, request):
        try:
            profile = request.user.profile
            projects = profile.projects.all()

            # Format dates for each project
            formatted_projects = []
            for project in projects:
                formatted_project = {
                    'title': project.title,
                    'description': project.description,
                    'tech_stack': project.tech_stack,
                    'project_type': project.get_project_type_display(),
                    'start_date': project.start_date.strftime("%Y-%m-%d") if project.start_date else "Not specified",
                    'end_date': project.end_date.strftime("%Y-%m-%d") if project.end_date else "Present",
                    'project_url': project.project_url,
                    'repo_url': project.repo_url,
                }
                formatted_projects.append(formatted_project)

            context = {
                'profile': profile,
                'projects': formatted_projects,
            }
        except Exception as e:
            print(f"Error loading portfolio data: {e}")
            context = {'error': "Failed to load portfolio data."}

        return render(request, self.template_name, context)
    
class UpdateHeaderView(LoginRequiredMixin, View):
    """
    Handles updating the header section of the portfolio.
    """
    def get(self, request):
        """
        Renders the form for GET requests.
        """
        try:
            profile = request.user.profile
            context = {
                'name': profile.name,
                'tagline': profile.tagline,
                'avatar': profile.avatar,
                'bio': profile.bio,
            }
        except ObjectDoesNotExist:
            context = {'error': "Profile not found. Please refresh the page."}

        return render(request, 'update-components/header.html', context)

    def post(self, request):
        """
        Processes form data for POST requests.
        """
        try:
            profile = request.user.profile

            # Update all fields from the form
            profile.name = request.POST.get('name')
            profile.tagline = request.POST.get('tagline')
            profile.avatar = request.POST.get('avatar')  # Add avatar field
            profile.bio = request.POST.get('bio')        # Add bio field

            # Save the updated profile
            profile.save()

            return redirect('portfolio_updater')  # Redirect back to the updater page
        except ObjectDoesNotExist:
            return JsonResponse({'error': "Profile not found. Please refresh the page."}, status=404)
        except Exception as e:
            print(f"Error updating header: {e}")
            return JsonResponse({'error': "Failed to update header."}, status=500)
        
class UpdateSkillsView(LoginRequiredMixin, View):
    """
    Handles adding new skills to the user's profile.
    """
    def post(self, request):
        """
        Processes form data for POST requests.
        """
        try:
            skill_name = request.POST.get('name')
            proficiency = request.POST.get('proficiency', 50)  # Default proficiency is 50%
            skill_type = request.POST.get('skill_type')
            category = request.POST.get('category')

            if skill_name:
                Skill.objects.create(
                    profile=request.user.profile,
                    name=skill_name,
                    proficiency=proficiency,
                    skill_type=skill_type,
                    category=category
                )
            return redirect('portfolio_updater')
        except ObjectDoesNotExist:
            return JsonResponse({'error': "Profile not found. Please refresh the page."}, status=404)
        except Exception as e:
            print(f"Error adding skill: {e}")
            return JsonResponse({'error': "Failed to add skill."}, status=500)


class UpdateProjectsView(LoginRequiredMixin, View):
    """
    Handles adding new projects to the user's profile.
    """
    def post(self, request):
        """
        Processes form data for POST requests.
        """
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            project_url = request.POST.get('project_url')
            repo_url = request.POST.get('repo_url')
            tech_stack = request.POST.get('tech_stack', '').split(',')  # Convert comma-separated string to list
            project_type = request.POST.get('project_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if title and description:
                Project.objects.create(
                    profile=request.user.profile,
                    title=title,
                    description=description,
                    project_url=project_url,
                    repo_url=repo_url,
                    tech_stack=tech_stack,
                    project_type=project_type,
                    start_date=start_date,
                    end_date=end_date
                )
            return redirect('portfolio_updater')
        except ObjectDoesNotExist:
            return JsonResponse({'error': "Profile not found. Please refresh the page."}, status=404)
        except Exception as e:
            print(f"Error adding project: {e}")
            return JsonResponse({'error': "Failed to add project."}, status=500)


# views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from .forms import ContactForm
from .models import Profile

class UpdateContactView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user

        # Ensure the profile exists
        profile, created = Profile.objects.get_or_create(user=user)

        # Process the form data
        form = ContactForm(request.POST, instance=profile)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # Update the User model's email field
            if email:
                user.email = email
                user.save()

            # Update the Profile model's phone field
            if phone or phone == "":  # Handle empty string for phone
                profile.phone = phone
                profile.save()

            messages.success(request, "Contact information updated successfully.")
        else:
            messages.error(request, "Please correct the errors below.")

        return redirect('portfolio_updater')


# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from .models import Profile, Skill, Project, Experience, SocialLink, Content, Interactive
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ProjectSerializer,
    ExperienceSerializer,
    SocialLinkSerializer,
    ContentSerializer,
    InteractiveSerializer,
)

class HomePageView(TemplateView):
    """
    View for rendering the homepage of the portfolio.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Fetch the user's profile (assuming one profile per user)
            profile = Profile.objects.first()
            
            if profile:
                # Fetch related data using optimized queries
                skills = profile.skills.all()
                projects = profile.projects.all()
                experiences = profile.experiences.all()
                social_links = profile.social_links.all()
                contents = profile.contents.all()
                interactive = getattr(profile, 'interactive', None)  # Handle one-to-one relationship

                # Serialize data for rendering or JavaScript consumption
                context['profile'] = ProfileSerializer(profile).data
                context['skills'] = SkillSerializer(skills, many=True).data
                context['projects'] = ProjectSerializer(projects, many=True).data
                context['experiences'] = ExperienceSerializer(experiences, many=True).data
                context['social_links'] = SocialLinkSerializer(social_links, many=True).data
                context['contents'] = ContentSerializer(contents, many=True).data
                context['interactive'] = InteractiveSerializer(interactive).data if interactive else None

            else:
                # Handle case where no profile exists
                context['error'] = "No profile data available."

        except Exception as e:
            # Log the error and provide a fallback message
            print(f"Error loading portfolio data: {e}")
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

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Experience
from .serializers import ExperienceSerializer

class ExperienceAPIView(APIView):
    """
    API View for fetching and updating Experience entries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        experiences = request.user.profile.experiences.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SocialLink
from .serializers import SocialLinkSerializer

class SocialLinksAPIView(APIView):
    """
    API View for fetching and updating Social Links entries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        social_links = request.user.profile.social_links.all()
        serializer = SocialLinkSerializer(social_links, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SocialLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Content
from .serializers import ContentSerializer

class ContentAPIView(APIView):
    """
    API View for fetching and updating Content entries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contents = request.user.profile.contents.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interactive
from .serializers import InteractiveSerializer

class InteractiveAPIView(APIView):
    """
    API View for fetching and updating Interactive Features.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interactive = request.user.profile.interactive
        serializer = InteractiveSerializer(interactive)
        return Response(serializer.data)

    def put(self, request):
        interactive = request.user.profile.interactive
        serializer = InteractiveSerializer(interactive, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)            

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
    
# views.py
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Experience

class UpdateExperienceView(LoginRequiredMixin, View):
    """
    Handles updating the Experience section of the portfolio.
    """
    def post(self, request):
        user = request.user
        profile = user.profile  # Ensure the profile exists

        # Create a new Experience entry
        Experience.objects.create(
            profile=profile,
            exp_type=request.POST.get('exp_type'),
            title=request.POST.get('title'),
            organization=request.POST.get('organization'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date') or None,  # Handle optional end_date
            description=request.POST.get('description', ''),
        )

        return redirect('portfolio_updater')  # Redirect back to the updater page


# views.py
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SocialLink

class UpdateSocialLinksView(LoginRequiredMixin, View):
    """
    Handles updating the Social Links section of the portfolio.
    """
    def post(self, request):
        user = request.user
        profile = user.profile  # Ensure the profile exists

        # Create a new SocialLink entry
        SocialLink.objects.create(
            profile=profile,
            platform=request.POST.get('platform'),
            url=request.POST.get('url'),
        )

        return redirect('portfolio_updater')  # Redirect back to the updater page

# views.py
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Content

class UpdateContentView(LoginRequiredMixin, View):
    """
    Handles updating the Content section of the portfolio.
    """
    def post(self, request):
        user = request.user
        profile = user.profile  # Ensure the profile exists

        # Create a new Content entry
        Content.objects.create(
            profile=profile,
            content_type=request.POST.get('content_type'),
            title=request.POST.get('title'),
            url=request.POST.get('url'),
            published_date=request.POST.get('published_date'),
            description=request.POST.get('description', ''),
        )

        return redirect('portfolio_updater')  # Redirect back to the updater page

# views.py
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Interactive

class UpdateInteractiveView(LoginRequiredMixin, View):
    """
    Handles updating the Interactive Features section of the portfolio.
    """
    def post(self, request):
        user = request.user
        profile = user.profile  # Ensure the profile exists

        # Get or create the Interactive object for the user
        interactive, created = Interactive.objects.get_or_create(profile=profile)

        # Update fields based on form input
        interactive.code_playground_enabled = 'code_playground_enabled' in request.POST
        interactive.live_streaming = 'live_streaming' in request.POST
        interactive.save()

        return redirect('portfolio_updater')  # Redirect back to the updater page                