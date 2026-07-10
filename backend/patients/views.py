from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .models import Patient
from .serializers import PatientSerializer


class PatientDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        return Response(PatientSerializer(patient).data)


class PatientHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        # reports/prescriptions/appointments serializers aren't wired in yet --
        # come back and fill these in once those apps' views exist
        data = {
            "patient": PatientSerializer(patient).data,
            "reports": [],
            "prescriptions": [],
            "past_appointments": [],
        }
        return Response(data)