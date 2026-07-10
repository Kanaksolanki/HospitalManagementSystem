from django.urls import path
from .views import BookAppointmentView, MyAppointmentsView, DoctorQueueView

urlpatterns = [
    path("", BookAppointmentView.as_view(), name="appointment-book"),
    path("mine/", MyAppointmentsView.as_view(), name="appointment-mine"),
    path("queue/", DoctorQueueView.as_view(), name="appointment-queue"),
]