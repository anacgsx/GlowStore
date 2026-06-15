from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Em produção acadêmica no Render, os arquivos de mídia de exemplo ficam no próprio projeto.
# Para um e-commerce real, o ideal seria Cloudinary/S3/Supabase Storage.
if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
