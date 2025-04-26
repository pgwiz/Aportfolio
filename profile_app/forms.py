# portfolio_app/forms.py
from django import forms
from .models import Profile, Skill, Project

class HeaderForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'tagline']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class ContactForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(required=False)