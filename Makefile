# Common dev tasks. Run `make help` to see them all.
PYTHON ?= python3
VENV   ?= .venv
ACTIVATE = . $(VENV)/bin/activate

.PHONY: help setup install migrate makemigrations seed run shell test check \
        collectstatic gunicorn daphne lint clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## One-shot bootstrap (venv + deps + migrate + seed demo data)
	./setup.sh

install: ## Create .venv (if missing) and install requirements
	@if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi
	$(ACTIVATE) && python -m pip install --upgrade pip && python -m pip install -r requirements.txt

migrate: ## Apply database migrations
	$(ACTIVATE) && python manage.py migrate

makemigrations: ## Generate new migration files
	$(ACTIVATE) && python manage.py makemigrations

seed: ## Seed demo profile + skills + projects + experience + content + social
	$(ACTIVATE) && python manage.py shell < scripts/seed_demo.py

run: ## Start the Django dev server
	$(ACTIVATE) && python manage.py runserver

shell: ## Open a Django shell
	$(ACTIVATE) && python manage.py shell

test: ## Run the test suite
	$(ACTIVATE) && python manage.py test

check: ## Run Django's system checks
	$(ACTIVATE) && python manage.py check

collectstatic: ## Collect static files into STATIC_ROOT (production-style)
	$(ACTIVATE) && python manage.py collectstatic --no-input

gunicorn: ## Run gunicorn against the WSGI app (Vercel-style)
	$(ACTIVATE) && gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000

daphne: ## Run daphne against the ASGI app (Render-style, supports WebSockets)
	$(ACTIVATE) && daphne -b 0.0.0.0 -p 8000 portfolio_project.asgi:application

clean: ## Remove venv + collected static files + sqlite db
	rm -rf $(VENV) staticfiles db.sqlite3 db.sqlite3-journal
