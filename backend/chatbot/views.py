from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from accounts.permissions import IsPatient
from patients.models import Patient
from appointments.models import Appointment
from prescriptions.models import Prescription
from reports.models import MedicalReport

from patient_chatbot import get_chat_response


class ChatView(APIView):
    """POST /api/chatbot/ -> {"message": "..."} -> {"reply": "..."}"""
    permission_classes = [IsPatient]

    def post(self, request):
        message = request.data.get("message", "").strip()
        if not message:
            return Response({"detail": "message is required"}, status=400)

        patient = Patient.objects.get(user=request.user)

        upcoming_appointments = list(
            Appointment.objects.filter(patient=patient, status="confirmed")
            .order_by("date")[:5]
            .values("date", "time", "doctor__user__username")
        )
        recent_prescriptions = list(
            Prescription.objects.filter(patient=patient)
            .order_by("-created_at")[:5]
            .values("medicines", "notes", "created_at")
        )
        recent_reports = list(
            MedicalReport.objects.filter(patient=patient)
            .order_by("-uploaded_date")[:5]
            .values("report_type", "ai_summary", "uploaded_date")
        )

        patient_context = {
            "name": patient.user.get_full_name() or patient.user.username,
            "upcoming_appointments": upcoming_appointments,
            "recent_prescriptions": recent_prescriptions,
            "recent_reports": recent_reports,
        }

        result = get_chat_response(message, patient_context)
        return Response(result)