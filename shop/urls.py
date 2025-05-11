"""
URL configuration for shop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
]

# Serve static and media files in debug mode and production for demo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
