from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time", "status", "reason")
    list_filter = ("status", "date", "doctor")
    search_fields = ("patient__patient_id", "doctor__doctor_id", "reason")
    date_hierarchy = "date"
    autocomplete_fields = ("patient", "doctor")
