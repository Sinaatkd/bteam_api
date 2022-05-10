from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# TODO: delete static urls in the production mode

urlpatterns = [
    path('sinabteamadmin/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('api-v1/', include('api_v1.urls')),
    path('api-v2/', include('api_v2.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)