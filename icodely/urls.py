from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from courses.views import page_not_found_404
from icodely import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("courses.urls"), name="courses"),
    path('cookies/', include('cookie_consent.urls')),
]

handler404 = page_not_found_404

if settings.DEBUG:
    urlpatterns = [
        path("exams/", include("examination.urls"), name="exam"),
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
