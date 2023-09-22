from django.urls import path

from examination import views

app_name = "examination"

urlpatterns = [
    path("<int:exam_id>/", views.exam_view, name="exam")
]
