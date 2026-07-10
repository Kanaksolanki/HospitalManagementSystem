from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from datetime import date

from .models import Appointment
from .serializers import AppointmentSerializer
from patients.models import Patient
from doctors.models import Doctor


class BookAppointmentView(APIView):
    """POST /api/appointments/ -> book a new appointment"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients can book appointments"}, status=403)

        doctor_id = request.data.get("doctor")
        doctor = Doctor.objects.filter(pk=doctor_id).first()
        if not doctor:
            return Response({"detail": "Doctor not found"}, status=404)

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=request.data.get("date"),
            time=request.data.get("time"),
            reason=request.data.get("reason", ""),
        )
        return Response(AppointmentSerializer(appointment).data, status=201)


class MyAppointmentsView(APIView):
    """GET /api/appointments/mine/ -> the logged-in patient's own appointments"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients have appointments here"}, status=403)

        appointments = Appointment.objects.filter(patient=patient)
        return Response(AppointmentSerializer(appointments, many=True).data)


class DoctorQueueView(APIView):
    """GET /api/appointments/queue/ -> today's queue for the logged-in doctor"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"detail": "Only doctors have a queue"}, status=403)

        appointments = Appointment.objects.filter(doctor=doctor, date=date.today())
        return Response(AppointmentSerializer(appointments, many=True).data)