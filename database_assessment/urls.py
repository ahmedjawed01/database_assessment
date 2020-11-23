from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bb_products.urls')),
    path('', include('populations.urls')),
    path('', include('custom_user.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
