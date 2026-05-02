#!/usr/bin/env bash
# Render build hook — installs deps, collects static assets, applies migrations.
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
