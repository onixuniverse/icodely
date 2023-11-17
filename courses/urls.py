from django.urls import path

from courses import views

app_name = "courses"

urlpatterns = [
    # path("", views.index_page, name="index"),

    path("", views.AllCoursesListView.as_view(), name="all_courses"),
    path("my/", views.MyCoursesListView.as_view(), name="my_courses"),
    path("<int:course_id>/", views.CourseDetailView.as_view(), name="course"),
    path("<int:course_id>/about/", views.AboutCourseDetailView.as_view(), name="about_course"),
    path("<int:course_id>/lessons/<int:lesson_id>/", views.LessonDetailView.as_view(), name="lesson"),

    path("<int:course_id>/lessons/<int:lesson_id>/homework/<int:homework_id>/",
         views.HomeworkDetailView.as_view(),
         name="homework"),

    path("deadlines/", views.DeadlineListView.as_view(), name="deadline"),

    path("invite/", views.invite_redirect, name="invite"),
    path("free/<int:course_id>/", views.free_course, name="free_course"),
]
