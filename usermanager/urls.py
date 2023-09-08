from django.urls import path

from usermanager import views

app_name = "usermanager"

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),

    path("signup/", views.RegistrationUser.as_view(), name="signup"),
    path("registration/", views.RegistrationUser.as_view()),

    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
]
