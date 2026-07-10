from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    message = "Only patients can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == "patient"
        )


class IsDoctor(BasePermission):
    message = "Only doctors can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == "doctor"
        )