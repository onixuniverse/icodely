from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_page, name="index"),

    path("courses/", views.AllCourses.as_view(), name="all_courses"),
    path("courses/my", views.MyCourses.as_view(), name="my_courses"),
    path("courses/teacher/my", views.TeachersCourses.as_view(), name="teacher_course"),
    path("courses/<int:course_id>/", views.ShowCourse.as_view(), name="course"),
    path("courses/<int:course_id>/lessons/<int:lesson_id>/", views.ShowLesson.as_view(), name="lesson"),
    # path("courses/<int:course_id>/lessons/<int:lesson_id>/test/<int:test_id>", views.Testing.as_view(),
    #      name="testing"),
    path("courses/new/", views.AddCourse.as_view(), name="addcourse"),
    path("courses/<int:course_id>/lessons/new/", views.AddLesson.as_view(), name="addlesson"),

    path("profile/me", views.ProfileView.as_view(), name="myaccount"),
    path("deadlines/", views.DeadlineView.as_view(), name="deadline"),

    path("registration/", views.RegistrationUser.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),

]
