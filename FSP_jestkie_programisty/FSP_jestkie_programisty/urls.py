from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('about/', include('about.urls')),
    path('feedback/', include('feedback.urls')),
    path('catalog/', include('catalog.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
