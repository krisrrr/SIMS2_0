from django.contrib import admin
from django.urls import path, include
from SIMS2_0.views import index_too
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index_too),
    path('admin/', admin.site.urls),
    path('activity/', include('activity.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
