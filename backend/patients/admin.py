from django.contrib import admin

from appointments.models import Appointment
from prescriptions.models import Prescription
from reports.models import MedicalReport

from .models import Patient


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    fields = ("doctor", "date", "time", "status", "reason")
    ordering = ("-date",)


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    fields = ("doctor", "created_at", "followup_date", "notes")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


class MedicalReportInline(admin.TabularInline):
    model = MedicalReport
    extra = 0
    fields = ("report_type", "uploaded_date", "hospital", "ai_summary")
    readonly_fields = ("uploaded_date",)
    ordering = ("-uploaded_date",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "get_full_name", "gender", "blood_group", "allergies", "created_at")
    list_filter = ("gender", "blood_group")
    search_fields = ("patient_id", "user__first_name", "user__last_name", "user__username", "allergies")
    readonly_fields = ("patient_id", "created_at")
    inlines = [AppointmentInline, PrescriptionInline, MedicalReportInline]

    @admin.display(description="Name")
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
