import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.handlers.wsgi import WSGIHandler
from django.urls import re_path
from django.views.static import serve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

# Custom WSGI app to handle both static and media files
class MediaFilesHandler(WSGIHandler):
    def __init__(self, application):
        self.application = application
        super().__init__()

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith(settings.MEDIA_URL):
            # Handle media files
            return serve(
                environ, start_response, 
                document_root=settings.MEDIA_ROOT,
                path=path[len(settings.MEDIA_URL):]
            )
        return self.application(environ, start_response)

# Use both static and media files handlers for development
application = get_wsgi_application()
app = StaticFilesHandler(MediaFilesHandler(application))
