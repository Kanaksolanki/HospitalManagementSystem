from django.urls import path
from .views import UploadReportView, MyReportsView

urlpatterns = [
    path("upload/", UploadReportView.as_view(), name="report-upload"),
    path("mine/", MyReportsView.as_view(), name="report-mine"),
]