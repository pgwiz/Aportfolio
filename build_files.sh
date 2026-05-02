#!/usr/bin/env bash
# Vercel @vercel/static-build entry: produce static assets for the deployment.
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
