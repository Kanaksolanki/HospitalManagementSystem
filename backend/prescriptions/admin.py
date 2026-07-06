from django.contrib import admin

from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "created_at", "followup_date")
    list_filter = ("doctor", "followup_date")
    search_fields = ("patient__patient_id", "doctor__doctor_id", "notes")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("patient", "doctor")
