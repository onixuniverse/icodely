from django.urls import path

from examination import views

app_name = "examination"

urlpatterns = [
    path("<int:exam_id>/", views.exam_view, name="exam"),
    path("<int:exam_id>/results/", views.ExamResultView.as_view(), name="exam_result"),

    path("wrong-user-answers/", views.wrong_answer_view)
]
