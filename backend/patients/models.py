from django.conf import settings
from django.db import models


class Patient(models.Model):
    """See PROJECT_PLAN.md Section 3 for the agreed schema."""

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    )

    # Human-friendly ID used everywhere in the frontend/contract, e.g. PID000145.
    # Auto-generated on first save — NOT concurrency-safe as written, which is fine
    # for a single-writer dev/demo setup. Swap for a UUID or DB sequence before
    # any real multi-user deployment.
    patient_id = models.CharField(max_length=12, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile"
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    insurance = models.CharField(max_length=100, blank=True)
    allergies = models.TextField(blank=True, help_text="Comma-separated known allergies")
    emergency_contact = models.CharField(max_length=20, blank=True)
    # Free-text list of prior diagnoses, e.g. ["Mild Anemia (2026)"] — kept simple
    # for MVP; could become its own model (PastDiagnosis) later if it needs dates
    # per entry, doctor attribution, etc.
    past_diseases = models.JSONField(default=list, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/patients/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by("-id").first()
            next_num = (last.id + 1) if last else 1
            self.patient_id = f"PID{next_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} - {self.user.get_full_name() or self.user.username}"
