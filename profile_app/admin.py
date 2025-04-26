# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    Profile,
    Skill,
    Project,
    Experience,
    SocialLink,
    Content,
    Interactive,
)

# Import the PortfolioUser model and its admin class from the authentication app
from authentication.models import PortfolioUser
from authentication.admin import UserAdmin as AuthenticationUserAdmin

# Custom Admin Classes

class ProfileInline(admin.StackedInline):
    """
    Inline admin for Profile to display alongside the User model.
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(AuthenticationUserAdmin):
    """
    Extend the custom admin for PortfolioUser to include Profile inline.
    """
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """
    list_display = ('user', 'name', 'tagline', 'updated_at')
    search_fields = ('name', 'tagline', 'bio')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'name', 'avatar', 'tagline')}),
        ('Details', {'fields': ('bio', 'updated_at')}),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Skill model.
    """
    list_display = ('name', 'profile', 'proficiency', 'skill_type', 'category')
    list_filter = ('skill_type', 'category')
    search_fields = ('name', 'category')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.
    """
    list_display = ('title', 'profile', 'project_type', 'start_date', 'end_date', 'tech_stack_display')
    list_filter = ('project_type', 'start_date')
    search_fields = ('title', 'description')

    def tech_stack_display(self, obj):
        """
        Display tech stack as a comma-separated string in the admin list view.
        """
        return ', '.join(obj.tech_stack) if obj.tech_stack else '-'
    tech_stack_display.short_description = 'Tech Stack'

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Experience model.
    """
    list_display = ('title', 'organization', 'exp_type', 'start_date', 'end_date')
    list_filter = ('exp_type', 'start_date')
    search_fields = ('title', 'organization')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SocialLink model.
    """
    list_display = ('platform', 'profile', 'url')
    list_filter = ('platform',)
    search_fields = ('url',)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Content model.
    """
    list_display = ('content_type', 'title', 'published_date')
    list_filter = ('content_type', 'published_date')
    search_fields = ('title', 'url')

@admin.register(Interactive)
class InteractiveAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Interactive model.
    """
    list_display = ('profile', 'code_playground_enabled', 'live_streaming', 'last_stream_start')
    list_filter = ('code_playground_enabled', 'live_streaming')
    readonly_fields = ('last_stream_start',)

# Unregister default Groups if needed
from django.contrib.auth.models import Group
admin.site.unregister(Group)

# Check if PortfolioUser is already registered before registering it again
if not admin.site.is_registered(PortfolioUser):
    admin.site.register(PortfolioUser, CustomUserAdmin)