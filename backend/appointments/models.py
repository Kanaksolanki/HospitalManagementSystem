from django.db import models

from doctors.models import Doctor
from patients.models import Patient


class Appointment(models.Model):
    """See PROJECT_PLAN.md Section 3 for the agreed schema."""

    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.CharField(max_length=20)  # e.g. "10:00 AM" — plain string is enough for MVP
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.patient.patient_id} with {self.doctor.doctor_id} on {self.date}"
