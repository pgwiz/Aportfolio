# Aportfolio

A Django-powered developer portfolio with a modern, responsive single-page UI.

The site renders a profile, skills, projects, experience, content, and social
links from a Postgres-backed admin, and exposes a JSON API for the same data
via Django REST Framework.

## Stack

- **Backend:** Django 5.2, Django REST Framework, Django Channels, drf-spectacular
- **Database:** Postgres (configured via `DATABASE_URL`)
- **Cache / channels:** Redis (in-memory layer by default; Redis layer commented in)
- **Frontend:** Server-rendered Django templates + a small vanilla CSS/JS design system (no build step)

## Project layout

```
authentication/    # Custom user model, registration, JWT auth
chat/              # Messages, notifications, channels routing
profile_app/       # Profile, Skill, Project, Experience, SocialLink, Content, Interactive models + viewsets
portfolio_project/ # Django settings, root URLs, ASGI/WSGI entrypoints
static/css/        # Design-system stylesheet
static/js/         # Theme toggle, scroll animations, background canvas
templates/         # base.html + index.html + components/*.html
```

## Quick start (local development)

1. Create and activate a virtualenv, then install requirements:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r req.txt
   ```

2. Provide the environment variables the app expects. Copy
   `portfolio_project/.env.example` to `.env` at the project root and fill it in:

   ```
   DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DB_NAME
   REDIS_URL=redis://localhost:6379
   ENCRYPTION_KEY=change-me
   ```

3. Migrate and run:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Open `http://localhost:8000/`. Sign in to `/admin/` to populate your
   profile, skills, projects, etc.

## API

OpenAPI schema is served by drf-spectacular:

- `GET /api/schema/` — raw OpenAPI document
- `GET /api/docs/` — Swagger UI

Domain endpoints live under `/api/portfolio/` and `/api/auth/`.

## Theming

The UI ships with a light and dark theme. The toggle button (top-right of the
nav) flips between them and the choice is persisted in `localStorage`. If the
user hasn't chosen, the site follows the OS-level
`prefers-color-scheme` preference.
