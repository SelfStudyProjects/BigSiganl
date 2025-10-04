from django.core.wsgi import get_wsgi_application
import os

# Use the project-level settings module. manage.py uses 'config.settings'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()