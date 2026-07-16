from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


def _generate_unique_username(base: str) -> str:
    """Turn an email local-part (or name) into a unique username, e.g.
    "riya.kapoor" -> "riya.kapoor", or "riya.kapoor2" if that's taken."""
    base = "".join(ch for ch in base.lower() if ch.isalnum() or ch in "._-") or "user"
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f"{base}{suffix}"
    return username


class RegisterSerializer(serializers.Serializer):
    """
    Matches the actual signup form: a single `name` field (split into
    first/last), email, phone, password, and role -- not Django's raw
    `username` field, which the frontend never collects. Doctor signups
    also require `specialization` (required on the Doctor model) and accept
    optional `qualification`/`experience`.
    """

    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    # Doctor-only fields -- validated conditionally in validate() below.
    specialization = serializers.CharField(max_length=100, required=False, allow_blank=True)
    qualification = serializers.CharField(max_length=150, required=False, allow_blank=True)
    experience = serializers.IntegerField(required=False, min_value=0, default=0)

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_password(self, value):
        # Enforces the project's AUTH_PASSWORD_VALIDATORS (min length, not
        # too common, not all-numeric, not too similar to the user's info).
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def validate(self, attrs):
        if attrs["role"] == "doctor" and not attrs.get("specialization"):
            raise serializers.ValidationError({"specialization": "Specialization is required for doctor accounts."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        name_parts = validated_data["name"].strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=_generate_unique_username(validated_data["email"].split("@")[0]),
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
            phone=validated_data.get("phone", ""),
            first_name=first_name,
            last_name=last_name,
        )

        if validated_data["role"] == "patient":
            from patients.models import Patient
            Patient.objects.create(user=user)
        else:
            from doctors.models import Doctor
            Doctor.objects.create(
                user=user,
                specialization=validated_data["specialization"],
                qualification=validated_data.get("qualification", ""),
                experience=validated_data.get("experience", 0),
                # Never trust the client for this, even if a request sends
                # is_approved -- it isn't even an accepted field here. Every
                # self-registered doctor starts unapproved; a hospital admin
                # flips this in the Django admin (doctors/admin.py already
                # surfaces it as a list_filter).
                is_approved=False,
            )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone", "first_name", "last_name"]


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login by email + password (matching API_CONTRACT.md's `{email, password}`
    shape) instead of Django's default `username` field, and adds `role` +
    `user_id` to the token response so the frontend can route straight to
    the right dashboard without a second request.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = serializers.EmailField()
        self.fields.pop("username", None)

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "No account found with that email."})

        # TokenObtainPairSerializer.validate() authenticates using whatever
        # key self.username_field points at (still "username" internally,
        # even though we removed it as an input field above) -- so we fill
        # it in ourselves from the looked-up user before calling super().
        attrs[self.username_field] = user.username
        data = super().validate(attrs)

        # Block login for doctors who haven't been approved yet -- this is
        # the actual security boundary; the frontend's "pending approval"
        # messaging is just UX on top of this.
        if self.user.role == "doctor":
            from doctors.models import Doctor
            doctor = Doctor.objects.filter(user=self.user).first()
            if not doctor or not doctor.is_approved:
                raise serializers.ValidationError(
                    {"detail": "Your doctor account is pending admin approval."}
                )

        data["role"] = self.user.role
        data["user_id"] = self.user.id
        return data