web: daphne -b 0.0.0.0 -p ${PORT:-8000} portfolio_project.asgi:application
release: python manage.py migrate --no-input
