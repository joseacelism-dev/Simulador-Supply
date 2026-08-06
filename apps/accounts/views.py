from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import StudentRegistrationForm


class HomeView(TemplateView):
    template_name = "home.html"


class StudentRegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy("accounts:student_dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:post_login_redirect")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class PostLoginRedirectView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin_docente:
            return redirect("accounts:teacher_dashboard")
        return redirect("accounts:student_dashboard")


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/student.html"


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin_docente


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_estudiante


class TeacherDashboardView(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = "dashboard/teacher.html"
