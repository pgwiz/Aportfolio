# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

PortfolioUser = get_user_model()

class RegistrationForm(forms.ModelForm):
    """
    Custom registration form for PortfolioUser.
    """
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        min_length=8,
        max_length=128,
        help_text="Your password must be at least 8 characters long."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        help_text="Enter the same password as above for verification."
    )

    class Meta:
        model = PortfolioUser
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }

    def clean_password2(self):
        """
        Validate that the two password fields match.
        """
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        """
        Save the user with the provided password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user