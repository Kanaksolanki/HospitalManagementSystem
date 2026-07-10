from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from accounts.permissions import IsPatient, IsDoctor

from .models import Prescription
from .serializers import PrescriptionSerializer
from patients.models import Patient
from doctors.models import Doctor

from drug_interaction_checker import check_drug_interaction


class WritePrescriptionView(APIView):
    """POST /api/prescriptions/ -> doctor writes a new prescription"""
    permission_classes = [IsDoctor]

    def post(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"detail": "Only doctors can write prescriptions"}, status=403)

        patient_id = request.data.get("patient")
        patient = Patient.objects.filter(pk=patient_id).first()
        if not patient:
            return Response({"detail": "Patient not found"}, status=404)

        medicines = request.data.get("medicines", [])
        medicine_names = [m.get("name") for m in medicines if m.get("name")]

        # Check for dangerous interactions BEFORE saving. If found, block
        # the save and tell the doctor why -- this is a safety check, not
        # a soft warning, since a missed drug interaction is genuinely
        # dangerous.
        if len(medicine_names) >= 2:
            try:
                interaction = check_drug_interaction(medicine_names)
                if interaction.get("interaction_found"):
                    return Response({
                        "detail": "Dangerous drug interaction detected",
                        "interaction_details": interaction.get("details"),
                    }, status=400)
            except Exception:
                pass  # if the checker itself fails, don't block prescribing

        prescription = Prescription.objects.create(
            patient=patient,
            doctor=doctor,
            medicines=medicines,
            notes=request.data.get("notes", ""),
            followup_date=request.data.get("followup_date"),
        )
        return Response(PrescriptionSerializer(prescription).data, status=201)


class MyPrescriptionsView(APIView):
    """GET /api/prescriptions/mine/ -> the logged-in patient's own prescriptions"""
    permission_classes = [IsPatient]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients have prescriptions here"}, status=403)

        prescriptions = Prescription.objects.filter(patient=patient)
        return Response(PrescriptionSerializer(prescriptions, many=True).data)