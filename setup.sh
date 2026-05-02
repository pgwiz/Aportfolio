#!/usr/bin/env bash
# One-shot local setup: creates a virtualenv, installs dependencies,
# applies migrations, and seeds demo data so you can `make run`
# immediately and see a populated portfolio.
set -e

PYTHON_BIN=${PYTHON_BIN:-python3}

if [ ! -d ".venv" ]; then
    echo ">> Creating virtualenv at .venv"
    "$PYTHON_BIN" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo ">> Upgrading pip"
python -m pip install --upgrade pip

echo ">> Installing requirements"
python -m pip install -r requirements.txt

if [ ! -f ".env" ]; then
    if [ -f "portfolio_project/.env.example" ]; then
        echo ">> Creating .env from portfolio_project/.env.example"
        cp portfolio_project/.env.example .env
    fi
fi

echo ">> Applying migrations"
python manage.py migrate --no-input

echo ">> Seeding demo data (idempotent)"
python manage.py shell < scripts/seed_demo.py

echo
echo "Setup complete."
echo
echo "Start the dev server with:"
echo "    source .venv/bin/activate && python manage.py runserver"
echo "or simply:"
echo "    make run"
