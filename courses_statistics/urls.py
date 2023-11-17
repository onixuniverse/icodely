from django.urls import path

from courses_statistics import views

app_name = "courses_statistics"

urlpatterns = [
    path('', views.get_statistics_data)
]