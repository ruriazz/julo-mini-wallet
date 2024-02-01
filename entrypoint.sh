python manage.py migrate && \
gunicorn 'core.wsgi:application' --bind 0.0.0.0:8000 --timeout 180 --worker-connections 1000