# profile_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import PortfolioUser
from .models import Profile

@receiver(post_save, sender=PortfolioUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile object when a new PortfolioUser is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=PortfolioUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile object when the PortfolioUser is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()