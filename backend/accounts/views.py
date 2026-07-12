from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer, EmailTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailLoginView(TokenObtainPairView):
    """POST /api/auth/login/ -> {email, password} => {access, refresh, role, user_id}"""
    serializer_class = EmailTokenObtainPairSerializer


class MeView(APIView):
    """
    GET /api/auth/me/ -> current user profile, plus the patient/doctor
    profile in one call (so the frontend doesn't need a second request to
    know a patient's displayed ID, blood group, etc, or a doctor's
    specialization/rating right after login).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user).data
        data["profile"] = None

        if request.user.role == "patient":
            from patients.models import Patient
            from patients.serializers import PatientSerializer
            patient = Patient.objects.filter(user=request.user).first()
            if patient:
                data["profile"] = PatientSerializer(patient).data
        elif request.user.role == "doctor":
            from doctors.models import Doctor
            from doctors.serializers import DoctorSerializer
            doctor = Doctor.objects.filter(user=request.user).first()
            if doctor:
                data["profile"] = DoctorSerializer(doctor).data

        return Response(data)