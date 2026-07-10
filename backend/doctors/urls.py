from django.urls import path
from .views import DoctorListView, DoctorSlotsView, DoctorSearchView

urlpatterns = [
    path("", DoctorListView.as_view(), name="doctor-list"),
    path("search/", DoctorSearchView.as_view(), name="doctor-search"),
    path("<int:pk>/slots/", DoctorSlotsView.as_view(), name="doctor-slots"),
]