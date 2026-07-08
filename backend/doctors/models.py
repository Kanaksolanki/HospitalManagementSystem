from django.db import models
from accounts.models import User


class Doctor(models.Model):
    doctor_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=200, blank=True)
    available_days = models.CharField(max_length=100, blank=True)  # e.g. "Mon,Wed,Fri"
    visiting_hours = models.CharField(max_length=100, blank=True)  # e.g. "10:00-14:00"
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            last = Doctor.objects.order_by("-id").first()
            next_num = (last.id + 1) if last else 1
            self.doctor_id = f"DOC{next_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor_id} - Dr. {self.user.username}"