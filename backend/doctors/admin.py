from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_id", "get_full_name", "specialization", "experience",
        "visiting_hours", "is_approved", "rating",
    )
    list_filter = ("specialization", "is_approved")
    search_fields = ("doctor_id", "user__first_name", "user__last_name", "user__username", "specialization")
    readonly_fields = ("doctor_id", "created_at")

    @admin.display(description="Name")
    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name() or obj.user.username}"
