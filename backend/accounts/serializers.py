from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "phone"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
            phone=validated_data.get("phone", ""),
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
        data["role"] = self.user.role
        data["user_id"] = self.user.id
        return data