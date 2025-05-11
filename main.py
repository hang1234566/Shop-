import os
from django.core.wsgi import get_wsgi_application

# Set Django's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

# Get the WSGI application
app = get_wsgi_application()
