# authentication/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class PortfolioUser(AbstractUser):
    # Add your custom fields here
    quick_id = models.CharField(max_length=20, blank=True, null=True)
    temp_password_hash = models.CharField(max_length=128, blank=True, null=True)

    # Add these to resolve the conflict
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="portfolio_user_groups",
        related_query_name="portfolio_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="portfolio_user_permissions",
        related_query_name="portfolio_user",
    )

    def generate_quick_credentials(self):
        # Your existing method
        pass
        
class UserPreference(models.Model):
    user = models.OneToOneField(PortfolioUser, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save()        