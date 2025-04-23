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

class ProjectSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['profile']

    def get_duration(self, obj):
        return f"{obj.start_date} - {obj.end_date or 'Present'}"

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