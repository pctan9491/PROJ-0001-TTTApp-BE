from rest_framework import serializers

from accounts.models import LoginCredential


class RegisterSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    gender = serializers.CharField(max_length=2)
    birth_date = serializers.DateField()

    username = serializers.CharField(max_length=70)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)



class LoginCredentialSerializer(serializers.Serializer):
    # Read-only representation of a LoginCredential row.
    # NOTE: `password_hash` is intentionally NOT included (never leak it).
    # Primary key of the login_credential row itself.
    id = serializers.UUIDField(read_only=True)
    # user_ulid is a FK to Users model -> serialize the related object's PK (UUID str).
    # Using `source='user_ulid.id'` reaches through the relation and pulls the UUID str
    # instead of the raw Users object (which would fail JSON serialization).
    user_ulid = serializers.UUIDField(source='user_ulid.id', read_only=True)
    # Plain char field on the model, no conversion needed.
    user_id = serializers.CharField(max_length=10, read_only=True)
    username = serializers.CharField(max_length=70, read_only=True)
    email = serializers.EmailField(max_length=100, read_only=True)
    enable_flag = serializers.BooleanField(read_only=True)
    # Model has blank=True, null=True -> serializer must accept None/empty string.
    biometric_info = serializers.CharField(
        max_length=100, allow_blank=True, allow_null=True, read_only=True,
    )
    # auth_ulid is a FK to Authentication -> same UUID-extraction trick as user_ulid.
    auth_ulid = serializers.UUIDField(source='auth_ulid.id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


