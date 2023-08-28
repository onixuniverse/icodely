from django.urls import path

from examination import views

urlpatterns = [
    path("e", views.exam_view)
]
