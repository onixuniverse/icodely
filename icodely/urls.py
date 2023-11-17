from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from icodely import settings

urlpatterns = [
    path("", include("base.urls", namespace="base")),
    path("courses/", include("courses.urls", namespace="courses")),
    path("admin/", admin.site.urls),
    path("exams/", include("examination.urls", namespace="examination")),
    path("profile/", include("usermanager.urls", namespace="usermanager")),
    # path("statistics/", include("courses_statistics.urls", namespace="statistics")),

    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('cookies/', include('cookie_consent.urls')),
]

handler403 = "courses.views.page_forbidden_403"
handler404 = "courses.views.page_not_found_404"
handler405 = "courses.views.page_method_not_allow_405"
handler500 = "courses.views.page_internal_error_500"

if settings.DEBUG:
    urlpatterns = [
                      # ...
                      path("__debug__/", include("debug_toolbar.urls")),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
