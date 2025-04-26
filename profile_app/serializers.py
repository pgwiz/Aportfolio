from rest_framework import serializers
from .models import Profile, Skill, Project, Experience, SocialLink, Content, Interactive

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'avatar', 'bio', 'tagline', 'updated_at']
        read_only_fields = ['user', 'updated_at']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['profile']
# serializers.py
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    """
    tech_stack = serializers.ListField(child=serializers.CharField())  # Ensure tech_stack is a list
    project_type_display = serializers.SerializerMethodField()  # Add human-readable project type

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'project_url',
            'repo_url',
            'tech_stack',
            'project_type',
            'project_type_display',  # Human-readable project type
            'start_date',
            'end_date',
        ]

    def get_project_type_display(self, obj):
        """
        Return the human-readable value of the project_type field.
        """
        return obj.get_project_type_display()
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['profile']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
        read_only_fields = ['profile']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['profile']

class InteractiveSerializer(serializers.ModelSerializer):
    streaming_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Interactive
        fields = '__all__'
        read_only_fields = ['profile']

    def get_streaming_status(self, obj):
        return "Live Now" if obj.live_streaming else "Offline"