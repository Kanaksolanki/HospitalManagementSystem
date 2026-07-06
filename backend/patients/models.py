from django.db import models
from accounts.models import User


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    )
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    patient_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    insurance = models.CharField(max_length=100, blank=True)
    allergies = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by("-id").first()
            next_num = (last.id + 1) if last else 1
            self.patient_id = f"PID{next_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} - {self.user.username}"