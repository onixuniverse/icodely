from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.index_page, name="index"),

    path("courses/", views.AllCoursesListView.as_view(), name="all_courses"),
    path("courses/my", views.MyCoursesListView.as_view(), name="my_courses"),
    path("courses/<int:course_id>/", views.CourseLessonsDetailView.as_view(), name="course"),
    path("courses/<int:course_id>/about/", views.AboutCourseDetailView.as_view(), name="about_course"),
    path("courses/<int:course_id>/lessons/<int:lesson_id>/", views.ShowLesson.as_view(), name="lesson"),

    path("courses/<int:course_id>/lessons/<int:lesson_id>/homework/<int:homework_id>/", views.HomeworkView.as_view(),
         name="homework"),

    # path("courses/teacher/my", views.TeachersCourses.as_view(), name="teacher_course"),
    # path("courses/new/", views.AddCourse.as_view(), name="addcourse"),
    # path("courses/<int:course_id>/lessons/new/", views.AddLesson.as_view(), name="addlesson"),

    path("deadlines/", views.DeadlineView.as_view(), name="deadline"),

    path("invite/", views.invite_redirect, name="invite"),
]
