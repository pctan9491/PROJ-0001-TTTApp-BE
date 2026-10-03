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


class LoginCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginCredential
        fields = (
            'id',
            'user_ulid',
            'user_id',
            'username',
            'email',
            'enable_flag',
            'biometric_info',
            'auth_ulid',
            'created_at',
        )
        read_only_fields = fields


