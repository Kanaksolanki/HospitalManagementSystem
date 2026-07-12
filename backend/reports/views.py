from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from accounts.permissions import IsPatient, IsDoctor
from accounts.permissions import IsPatient

from .models import MedicalReport
from .serializers import MedicalReportSerializer
from patients.models import Patient

from report_summarizer import summarize_report
from ocr_extractor import extract_report_text


class UploadReportView(APIView):
    """POST /api/reports/upload/ -> patient uploads a new report"""
    permission_classes = [IsPatient]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients can upload reports"}, status=403)

        uploaded_file = request.FILES.get("file")
        raw_text = (request.data.get("raw_text") or "").strip()
        ocr_method = "typed" if raw_text else ""
        ocr_error = None

        # If the patient didn't type/paste the text themselves, try reading
        # it straight from the uploaded file -- a real text layer for PDFs
        # exported by a lab, or OCR for a scanned PDF / phone photo.
        if not raw_text and uploaded_file:
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)  # rewind so it can still be saved to disk below
            ocr_result = extract_report_text(
                file_bytes, filename=uploaded_file.name, content_type=uploaded_file.content_type,
            )
            raw_text = ocr_result["text"]
            ocr_method = ocr_result["method"] or ""
            ocr_error = ocr_result["error"]

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
            file=uploaded_file,
            hospital=request.data.get("hospital", ""),
            raw_text=raw_text,
            ocr_method=ocr_method,
            ai_summary=ai_summary,
            ai_flags=ai_flags,
        )
        data = MedicalReportSerializer(report).data
        if ocr_error:
            data["ocr_error"] = ocr_error
        return Response(data, status=201)


class MyReportsView(APIView):
    """GET /api/reports/mine/ -> the logged-in patient's own reports"""
    permission_classes = [IsPatient]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Only patients have reports here"}, status=403)

        reports = MedicalReport.objects.filter(patient=patient)
        return Response(MedicalReportSerializer(reports, many=True).data)