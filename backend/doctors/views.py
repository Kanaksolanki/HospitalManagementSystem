from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from accounts.permissions import IsDoctor
from django.shortcuts import get_object_or_404

from .models import Doctor
from .serializers import DoctorSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer


class DoctorListView(APIView):
    """GET /api/doctors/ -> list all doctors, optional ?specialization=... filter"""
    permission_classes = [IsDoctor]

    def get(self, request):
        doctors = Doctor.objects.filter(is_approved=True)
        specialization = request.query_params.get("specialization")
        if specialization:
            doctors = doctors.filter(specialization__iexact=specialization)
        return Response(DoctorSerializer(doctors, many=True).data)


class DoctorSlotsView(APIView):
    """GET /api/doctors/<id>/slots/ -> available time slots for a doctor"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        # available_days is a JSONField list like ["Mon", "Wed", "Fri"]
        # visiting_hours is a plain string like "10:00-14:00"
        # Real slot-splitting (e.g. into 30-min chunks) isn't built yet --
        # returning the raw day/hour info is enough for the frontend to
        # show something real for now.
        return Response({
            "doctor_id": doctor.doctor_id,
            "available_days": doctor.available_days,
            "visiting_hours": doctor.visiting_hours,
        })


class DoctorSearchView(APIView):
    """GET /api/doctors/search/?patient_id=PID000145 -> find a patient (doctor-facing lookup)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response({"detail": "patient_id query param is required"}, status=400)
        patient = get_object_or_404(Patient, patient_id=patient_id)
        return Response(PatientSerializer(patient).data)