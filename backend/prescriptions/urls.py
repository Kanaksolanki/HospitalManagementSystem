from django.urls import path
from .views import WritePrescriptionView, MyPrescriptionsView

urlpatterns = [
    path("", WritePrescriptionView.as_view(), name="prescription-write"),
    path("mine/", MyPrescriptionsView.as_view(), name="prescription-mine"),
]