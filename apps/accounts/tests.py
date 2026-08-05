from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountsFlowTests(TestCase):
    def test_student_registration_creates_student_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "estudiante1",
                "first_name": "Ana",
                "last_name": "Perez",
                "email": "ana@example.com",
                "password1": "ClaveSegura123!",
                "password2": "ClaveSegura123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:student_dashboard"))
        user = User.objects.get(username="estudiante1")
        self.assertEqual(user.role, User.Role.ESTUDIANTE)

    def test_anonymous_user_cannot_access_student_dashboard(self):
        response = self.client.get(reverse("accounts:student_dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_student_cannot_access_teacher_dashboard(self):
        user = User.objects.create_user(
            username="estudiante2",
            password="ClaveSegura123!",
            role=User.Role.ESTUDIANTE,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:teacher_dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_teacher_dashboard(self):
        user = User.objects.create_user(
            username="docente",
            password="ClaveSegura123!",
            role=User.Role.ADMIN_DOCENTE,
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:teacher_dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_post_login_redirect_sends_student_to_student_dashboard(self):
        user = User.objects.create_user(
            username="estudiante3",
            password="ClaveSegura123!",
            role=User.Role.ESTUDIANTE,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:post_login_redirect"))

        self.assertRedirects(response, reverse("accounts:student_dashboard"))

