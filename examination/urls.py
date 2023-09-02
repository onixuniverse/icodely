from django.urls import path

from examination import views

app_name = "examination"

urlpatterns = [
    path("e", views.exam_view)
]
