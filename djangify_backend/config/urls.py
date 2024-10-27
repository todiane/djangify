# djangify_backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from djangify_backend.apps.core.views import home


urlpatterns = [
    path('', home, name='home'),  # Homepage URL
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('api/v1/blog/', include('djangify_backend.apps.blog.urls')),
    path('api/v1/portfolio/', include('djangify_backend.apps.portfolio.urls')),
    # API documentation endpoints
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
