from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from icodely import settings

urlpatterns = [
    path("", include("courses.urls", namespace="courses")),
    path("admin/", admin.site.urls),
    path("exams/", include("examination.urls", namespace="examination")),
    path("profile/", include("usermanager.urls", namespace="usermanager")),

    path('cookies/', include('cookie_consent.urls')),
]

handler404 = "courses.views.page_not_found_404"

if settings.DEBUG:
    urlpatterns = [
                      # ...
                      path("__debug__/", include("debug_toolbar.urls")),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
