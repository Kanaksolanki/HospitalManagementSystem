from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id", "doctor_id", "full_name", "specialization",
            "experience", "qualification", "available_days",
            "visiting_hours", "is_approved", "rating",
        ]
        read_only_fields = ["id", "doctor_id"]

    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name() or obj.user.username}"
