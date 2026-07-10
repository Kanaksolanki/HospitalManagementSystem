from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import MedicalReport
from .serializers import MedicalReportSerializer
from patients.models import Patient

from report_summarizer import summarize_report


class UploadReportView(APIView):
    """POST /api/reports/upload/ -> patient uploads a new report"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients can upload reports"}, status=403)

        raw_text = request.data.get("raw_text", "")

        # Run the AI summarizer if we have text to work with. This never
        # blocks the upload if it fails -- a report should still save even
        # if summarization has a problem.
        ai_summary = ""
        ai_flags = []
        if raw_text:
            try:
                result = summarize_report(raw_text)
                ai_summary = result.get("summary", "")
                ai_flags = result.get("flags", [])
            except Exception:
                pass  # report still saves without AI summary

        report = MedicalReport.objects.create(
            patient=patient,
            report_type=request.data.get("report_type", ""),
            file=request.FILES.get("file"),
            hospital=request.data.get("hospital", ""),
            raw_text=raw_text,
            ai_summary=ai_summary,
            ai_flags=ai_flags,
        )
        return Response(MedicalReportSerializer(report).data, status=201)


class MyReportsView(APIView):
    """GET /api/reports/mine/ -> the logged-in patient's own reports"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients have reports here"}, status=403)

        reports = MedicalReport.objects.filter(patient=patient)
        return Response(MedicalReportSerializer(reports, many=True).data)