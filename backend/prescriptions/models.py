from django.db import models

from doctors.models import Doctor
from patients.models import Patient


class Prescription(models.Model):
    """See PROJECT_PLAN.md Section 3 for the agreed schema."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="prescriptions")
    medicines = models.JSONField(
        default=list,
        help_text='[{"name": "...", "dosage": "...", "frequency": "..."}]',
    )
    notes = models.TextField(blank=True)
    followup_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rx for {self.patient.patient_id} by {self.doctor.doctor_id} on {self.created_at.date()}"
