from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN_DOCENTE = "admin_docente", "Administrador docente"
        ESTUDIANTE = "estudiante", "Estudiante"

    role = models.CharField(
        "rol",
        max_length=30,
        choices=Role.choices,
        default=Role.ESTUDIANTE,
    )

    @property
    def is_admin_docente(self):
        return self.role == self.Role.ADMIN_DOCENTE

    @property
    def is_estudiante(self):
        return self.role == self.Role.ESTUDIANTE

