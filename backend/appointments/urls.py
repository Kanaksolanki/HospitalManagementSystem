from django.urls import path
from .views import BookAppointmentView, MyAppointmentsView, DoctorQueueView, DoctorAppointmentsView

urlpatterns = [
    path("", BookAppointmentView.as_view(), name="appointment-book"),
    path("mine/", MyAppointmentsView.as_view(), name="appointment-mine"),
    path("queue/", DoctorQueueView.as_view(), name="appointment-queue"),
    path("doctor-mine/", DoctorAppointmentsView.as_view(), name="appointment-doctor-mine"),
]