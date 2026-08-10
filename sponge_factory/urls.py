from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from shop.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('shop.urls')),
]

# Development rejimida media va static fayllarni xizmat qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'shop.views.custom_404'
handler500 = 'shop.views.custom_500'
