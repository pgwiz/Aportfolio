"""Seed demo data into a fresh sqlite database for local testing.

Usage:
    python manage.py shell < scripts/seed_demo.py
"""
from datetime import date, datetime, timezone
from django.contrib.auth import get_user_model

from profile_app.models import (
    Profile, Skill, Project, Experience, SocialLink, Content, Interactive
)

User = get_user_model()

USERNAME = "demo"
EMAIL = "demo@example.com"

user, created = User.objects.get_or_create(
    username=USERNAME,
    defaults={"email": EMAIL, "is_staff": True, "is_superuser": True},
)
if created:
    user.set_password("demo-password")
    user.save()
    print(f"Created user: {USERNAME} (password: demo-password)")
else:
    user.email = EMAIL
    user.save()
    print(f"Reusing user: {USERNAME}")

# A Profile is auto-created by post_save on PortfolioUser, so we
# update it instead of relying on get_or_create defaults.
profile, _ = Profile.objects.get_or_create(user=user)
profile.name = "Peter Brian"
profile.tagline = "Full-stack developer · Django + modern web"
profile.avatar = ""
profile.bio = (
    "I'm a software engineer who likes building practical, "
    "well-tested products. This portfolio collects the projects, "
    "writing, and experience I'm most proud of."
)
profile.phone = ""
profile.save()

profile.skills.all().delete()
profile.projects.all().delete()
profile.experiences.all().delete()
profile.social_links.all().delete()
profile.contents.all().delete()
Interactive.objects.filter(profile=profile).delete()

skills = [
    ("Python", 92, "TECH", "Backend"),
    ("Django", 88, "TECH", "Backend"),
    ("PostgreSQL", 80, "TECH", "Data"),
    ("TypeScript", 78, "TECH", "Frontend"),
    ("React", 70, "TECH", "Frontend"),
    ("CSS / design systems", 75, "TECH", "Frontend"),
    ("Docker", 65, "TOOL", "DevOps"),
    ("Communication", 90, "SOFT", "People"),
]
for name, prof, kind, category in skills:
    Skill.objects.create(
        profile=profile,
        name=name,
        proficiency=prof,
        skill_type=kind,
        category=category,
    )

Project.objects.create(
    profile=profile,
    title="Aportfolio",
    description="A Django-powered developer portfolio with a modern, themable UI.",
    project_url="https://github.com/pgwiz/Aportfolio",
    repo_url="https://github.com/pgwiz/Aportfolio",
    tech_stack=["Python", "Django", "DRF", "Vanilla JS"],
    project_type="OS",
    start_date=date(2025, 3, 1),
    end_date=None,
)
Project.objects.create(
    profile=profile,
    title="Realtime chat playground",
    description="An exploration of Django Channels with a tidy frontend.",
    project_url="https://example.com/chat",
    repo_url="",
    tech_stack=["Django Channels", "Redis", "WebSockets"],
    project_type="EXPR",
    start_date=date(2024, 9, 1),
    end_date=date(2025, 1, 30),
)
Project.objects.create(
    profile=profile,
    title="Telegram portfolio sync",
    description="Bot + integration that mirrors portfolio updates to Telegram.",
    project_url="https://example.com/telegram",
    repo_url="https://github.com/example/telegram-portfolio",
    tech_stack=["Python", "Telegram Bot API", "Celery"],
    project_type="LIVE",
    start_date=date(2024, 4, 1),
    end_date=None,
)

Experience.objects.create(
    profile=profile,
    exp_type="PRO",
    title="Senior Software Engineer",
    organization="Independent / freelance",
    start_date=date(2022, 1, 1),
    end_date=None,
    description="Designing and shipping web products end-to-end across the stack.",
)
Experience.objects.create(
    profile=profile,
    exp_type="EDU",
    title="BSc Computer Science",
    organization="University",
    start_date=date(2018, 9, 1),
    end_date=date(2022, 6, 30),
    description="Focus on systems, distributed computing, and HCI.",
)

SocialLink.objects.create(profile=profile, platform="GH", url="https://github.com/pgwiz")
SocialLink.objects.create(profile=profile, platform="LI", url="https://www.linkedin.com/in/peter-brian-68b7ab2a1/")
SocialLink.objects.create(profile=profile, platform="TG", url="https://t.me/example")

Content.objects.create(
    profile=profile,
    content_type="BLOG",
    title="Designing a small Django design system",
    url="https://example.com/blog/django-design-system",
    published_date=date(2025, 2, 14),
    description="Notes from rebuilding the look-and-feel of this portfolio with CSS variables and a single-file design system.",
)

Interactive.objects.create(
    profile=profile,
    code_playground_enabled=True,
    live_streaming=False,
    last_stream_start=datetime(2025, 1, 12, 18, 0, tzinfo=timezone.utc),
    active_challenges=["Advent of Code 2024", "Build-in-public weekend"],
)

print("Seeded profile + skills + projects + experience + content + social links + interactive.")
