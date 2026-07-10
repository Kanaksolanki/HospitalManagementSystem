from rest_framework import serializers
from .models import MedicalReport


class MedicalReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalReport
        fields = [
            "id", "patient", "patient_name", "report_type", "file",
            "hospital", "uploaded_date", "raw_text", "ai_summary", "ai_flags",
        ]
        read_only_fields = ["id", "uploaded_date", "ai_summary", "ai_flags"]

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username