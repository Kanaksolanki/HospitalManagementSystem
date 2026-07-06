from rest_framework import serializers

# Define DRF serializers here.
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id", "patient_id", "username", "email",
            "dob", "gender", "blood_group", "address",
            "insurance", "allergies", "emergency_contact",
        ]
        read_only_fields = ["id", "patient_id"]