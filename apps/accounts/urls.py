from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    PostLoginRedirectView,
    StudentDashboardView,
    StudentRegistrationView,
    TeacherDashboardView,
)


app_name = "accounts"

urlpatterns = [
    path("registro/", StudentRegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirigir/", PostLoginRedirectView.as_view(), name="post_login_redirect"),
    path("panel/estudiante/", StudentDashboardView.as_view(), name="student_dashboard"),
    path("panel/docente/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
]

