from django.contrib import admin

from .models import MedicalReport


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ("patient", "report_type", "hospital", "uploaded_date", "flag_count")
    list_filter = ("report_type", "hospital", "uploaded_date")
    search_fields = ("patient__patient_id", "report_type", "raw_text")
    readonly_fields = ("uploaded_date",)
    autocomplete_fields = ("patient",)

    @admin.display(description="Flags")
    def flag_count(self, obj):
        return len(obj.ai_flags) if obj.ai_flags else 0
