# Aportfolio

A Django-powered developer portfolio with a modern, responsive single-page UI.

The site renders a profile, skills, projects, experience, content, and social
links from the database, and exposes a JSON API for the same data via Django
REST Framework. WebSockets / Django Channels back the optional chat feature.

## Stack

- **Backend:** Django 5.2, Django REST Framework, Django Channels, drf-spectacular
- **Database:** Postgres in production (`DATABASE_URL`), sqlite locally when no env is set
- **Cache / channels:** Redis (`REDIS_URL`), with an in-memory fallback for dev
- **Frontend:** Server-rendered Django templates + a small vanilla CSS/JS design system (no build step)
- **Static files:** Served by [WhiteNoise](https://whitenoise.readthedocs.io/) in production

## Project layout

```
authentication/    # Custom user model, registration, JWT auth
chat/              # Messages, notifications, channels routing
profile_app/       # Profile, Skill, Project, Experience, SocialLink, Content, Interactive
portfolio_project/ # Django settings, root URLs, ASGI/WSGI entrypoints
static/css/        # Design-system stylesheet
static/js/         # Theme toggle, scroll animations, background canvas
templates/         # base.html + index.html + components/*.html
scripts/           # One-off helpers (e.g. seed_demo.py)
```

## Quick start

The fastest path — creates a virtualenv, installs deps, applies migrations, and
seeds a demo profile:

```bash
./setup.sh
make run
```

…then open <http://localhost:8000/>. Sign in at `/login/` with
`demo` / `demo-password` to swap the nav's "Log in" for an "Edit" link to
`/portfolio_updater/`.

If you'd rather drive things by hand:

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`make help` lists every available task (`install`, `migrate`, `seed`, `run`,
`shell`, `test`, `check`, `collectstatic`, `gunicorn`, `daphne`, `clean`).

## Configuration

Configuration is read from environment variables. Copy
[`portfolio_project/.env.example`](portfolio_project/.env.example) to `.env`
at the project root and fill it in:

| Variable                | What it does                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| `SECRET_KEY`            | Django secret key. **Required in production.** A `django-insecure-…` fallback is used in dev.       |
| `DEBUG`                 | `true`/`false`. Defaults to `true` for local development.                                           |
| `ALLOWED_HOSTS`         | Comma-separated list. Defaults to `localhost,127.0.0.1,0.0.0.0`.                                    |
| `DATABASE_URL`          | `postgres://USER:PASSWORD@HOST:5432/DB`. **Unset → falls back to a local sqlite file.**             |
| `REDIS_URL`             | `redis://…`. Used by Channels' Redis layer when enabled.                                            |
| `CSRF_TRUSTED_ORIGINS`  | Comma-separated, e.g. `https://www.example.com`. Auto-extended with the platform-provided hostname. |

## Deployment

### Render (recommended — supports WebSockets)

1. Push this repo to GitHub.
2. In Render, click **New → Blueprint** and select the repo. Render will read
   [`render.yaml`](render.yaml) and provision:
   - a free Postgres database
   - a free Redis instance
   - a web service running Daphne (so Channels/WebSockets work)
3. The blueprint generates a `SECRET_KEY` automatically and wires
   `DATABASE_URL`, `REDIS_URL`, and `RENDER_EXTERNAL_HOSTNAME` for you. The
   build step ([`build.sh`](build.sh)) installs deps, collects static files,
   and applies migrations.
4. Once the service is live, optionally `render exec` into the web instance to
   create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Vercel (REST + homepage only — WebSockets not supported)

[`vercel.json`](vercel.json) routes all requests to the Django WSGI app via
`@vercel/python` and runs `build_files.sh` to collect static files.

1. Install the Vercel CLI (`npm i -g vercel`) and run `vercel link`.
2. Set the required env vars in **Project Settings → Environment Variables**:
   - `SECRET_KEY` — generate something secure
   - `DEBUG=false`
   - `DATABASE_URL` — point at a hosted Postgres (Vercel Postgres, Neon, Supabase, etc.)
   - `ALLOWED_HOSTS` — `your-project.vercel.app` (or your custom domain)
3. Deploy:
   ```bash
   vercel --prod
   ```

> **Heads up:** Vercel's serverless model doesn't run persistent WebSocket
> connections, so the `chat` Channels routes won't work there. The homepage,
> the REST API (`/api/…`), and the OpenAPI docs work fine. If you need
> Channels in production, deploy to Render (or any host that runs Daphne /
> Uvicorn long-lived).

### Procfile-based hosts (Heroku, Railway, Fly.io)

[`Procfile`](Procfile) declares a `web` process that runs Daphne and a
`release` step that applies migrations. Set the same env vars described in
**Configuration** above.

## API

OpenAPI schema is served by drf-spectacular:

- `GET /api/schema/` — raw OpenAPI document
- `GET /api/docs/` — Swagger UI

Domain endpoints live under `/api/portfolio/` and `/api/auth/`.

## Theming

The UI ships with a light and dark theme. The toggle button (top-right of the
nav) flips between them and the choice is persisted in `localStorage`. If the
user hasn't chosen, the site follows the OS-level `prefers-color-scheme`
preference.
