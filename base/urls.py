from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index_page, name="index")
]