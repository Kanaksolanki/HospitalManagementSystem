from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    # Login is by email (see EmailTokenObtainPairSerializer), so this has to
    # be unique -- Django's AbstractUser doesn't enforce that by default.
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"