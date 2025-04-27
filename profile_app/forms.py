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


class ContactForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Email field from the User model
    phone = forms.CharField(max_length=15, required=False)  # Phone field from the Profile model

    class Meta:
        model = Profile
        fields = ['phone']  # Only include Profile-specific fields here

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pass the user instance to the form
        super().__init__(*args, **kwargs)

        # Pre-fill the email field with the current user's email
        if self.user:
            self.fields['email'].initial = self.user.email