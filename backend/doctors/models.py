from django.conf import settings
from django.db import models


class Doctor(models.Model):
    """See PROJECT_PLAN.md Section 3 for the agreed schema."""

    doctor_id = models.CharField(max_length=12, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    qualification = models.CharField(max_length=150, blank=True)
    available_days = models.JSONField(default=list, help_text='e.g. ["Mon", "Wed", "Fri"]')
    visiting_hours = models.CharField(max_length=50, blank=True)
    is_approved = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    profile_picture = models.ImageField(upload_to="profile_pics/doctors/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            last = Doctor.objects.order_by("-id").first()
            next_num = (last.id + 1) if last else 1
            self.doctor_id = f"DOC{next_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor_id} - Dr. {self.user.get_full_name() or self.user.username}"
