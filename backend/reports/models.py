from django.db import models

from patients.models import Patient


def report_upload_path(instance, filename):
    return f"reports/{instance.patient.patient_id}/{filename}"


class MedicalReport(models.Model):
    """See PROJECT_PLAN.md Section 3 for the agreed schema."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    report_type = models.CharField(max_length=100)  # e.g. "Blood Test (CBC)", "X-Ray", "ECG"
    file = models.FileField(upload_to=report_upload_path)
    hospital = models.CharField(max_length=150, blank=True)
    uploaded_date = models.DateField(auto_now_add=True)
    # Extracted/typed text used as input to the AI summarizer. In production this
    # would come from OCR on the uploaded file; for MVP it's populated directly
    # (typed at upload time, or filled in by the seed script for sample data).
    raw_text = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    ai_flags = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-uploaded_date"]

    def __str__(self):
        return f"{self.report_type} - {self.patient.patient_id}"
