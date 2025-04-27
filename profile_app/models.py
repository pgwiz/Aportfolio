# models.py
from django.db import models
from authentication.models import PortfolioUser

# models.py
from django.db import models
from authentication.models import PortfolioUser

class Profile(models.Model):
    user = models.OneToOneField(PortfolioUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    avatar = models.URLField(max_length=500)
    bio = models.TextField(max_length=2000)
    tagline = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Added phone field
    updated_at = models.DateTimeField(auto_now=True)
    
class Skill(models.Model):
    SKILL_TYPES = (
        ('TECH', 'Technical'),
        ('TOOL', 'Tool'),
        ('SOFT', 'Soft Skill'),
        ('LANG', 'Language'),
    )
    
    profile = models.ForeignKey(Profile, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    proficiency = models.IntegerField(default=50)  # 0-100%
    skill_type = models.CharField(max_length=4, choices=SKILL_TYPES)
    category = models.CharField(max_length=50)  # e.g., "Frontend", "DevOps"

class Project(models.Model):
    PROJECT_TYPES = (
        ('LIVE', 'Live Project'),
        ('ARCH', 'Archived'),
        ('EXPR', 'Experiment'),
        ('OS', 'Open Source'),
    )
    
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField()
    repo_url = models.URLField(blank=True)
    tech_stack = models.JSONField()  # ["Python", "Django", "React"]
    project_type = models.CharField(max_length=4, choices=PROJECT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Experience(models.Model):
    EXP_TYPES = (
        ('PRO', 'Professional'),
        ('EDU', 'Education'),
        ('CERT', 'Certification'),
        ('ACHV', 'Achievement'),
    )
    
    profile = models.ForeignKey(Profile, related_name='experiences', on_delete=models.CASCADE)
    exp_type = models.CharField(max_length=4, choices=EXP_TYPES)
    title = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

class SocialLink(models.Model):
    PLATFORMS = (
        ('GH', 'GitHub'),
        ('LI', 'LinkedIn'),
        ('TW', 'Twitter'),
        ('TG', 'Telegram'),
    )
    
    profile = models.ForeignKey(Profile, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORMS)
    url = models.URLField()

class Content(models.Model):
    CONTENT_TYPES = (
        ('BLOG', 'Blog Post'),
        ('WRITE', 'Technical Writing'),
        ('VIDEO', 'Video Demo'),
        ('DECK', 'Presentation'),
    )
    
    profile = models.ForeignKey(Profile, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200)
    url = models.URLField()
    published_date = models.DateField()
    description = models.TextField()

class Interactive(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    code_playground_enabled = models.BooleanField(default=False)
    live_streaming = models.BooleanField(default=False)
    last_stream_start = models.DateTimeField(null=True)
    active_challenges = models.JSONField(default=list)