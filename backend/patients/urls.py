from django.urls import path
from .views import PatientDetailView, PatientHistoryView

urlpatterns = [
    path("<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),
    path("<int:pk>/history/", PatientHistoryView.as_view(), name="patient-history"),
]