from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, UserSerializer, EmailTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        if user.role == "doctor":
            # No tokens issued -- an unapproved doctor account can't do
            # anything with them anyway (see EmailTokenObtainPairSerializer),
            # so don't hand out a token that mostly doesn't work.
            return Response({
                "role": user.role,
                "user_id": user.id,
                "is_approved": False,
                "detail": "Account created. A hospital admin needs to approve your account before you can log in.",
            }, status=status.HTTP_201_CREATED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
            "user_id": user.id,
        }, status=status.HTTP_201_CREATED)


class EmailLoginView(TokenObtainPairView):
    """POST /api/auth/login/ -> {email, password} => {access, refresh, role, user_id}"""
    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class LogoutView(APIView):
    """
    POST /api/auth/logout/ -> {refresh} => 205

    Blacklists the refresh token server-side so it can't be reused even if
    someone captured it -- just deleting tokens client-side doesn't actually
    revoke them. Requires rest_framework_simplejwt.token_blacklist in
    INSTALLED_APPS (see settings.py).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            # Already invalid/expired/blacklisted -- logout still "succeeds"
            # from the client's point of view, nothing more to revoke.
            pass
        return Response(status=status.HTTP_205_RESET_CONTENT)


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