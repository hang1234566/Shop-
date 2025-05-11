import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

if settings.DEBUG:
    app = StaticFilesHandler(get_wsgi_application())
else:
    app = get_wsgi_application()
