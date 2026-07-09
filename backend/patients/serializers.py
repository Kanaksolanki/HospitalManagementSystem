from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id", "patient_id", "full_name", "dob", "gender",
            "blood_group", "address", "insurance", "allergies",
            "emergency_contact", "past_diseases",
        ]
        read_only_fields = ["id", "patient_id"]

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username