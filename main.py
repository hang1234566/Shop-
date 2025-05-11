import os
from shop.wsgi import application

# Define the Flask WSGI app for gunicorn to use
app = application
