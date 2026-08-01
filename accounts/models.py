from django.db import models

from accounts.uuidv7 import uuidv7


class Authentication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    auth_path = models.CharField(max_length=30)

    class Meta:
        db_table = 'Authentication'
        managed = False


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    user_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    gender = models.CharField(max_length=2)
    birth_date = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    class Meta:
        db_table = 'Users'
        managed = False


class LoginCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    user_ulid = models.ForeignKey(
        Users,
        db_column='user_ulid',
        to_field='id',
        on_delete=models.CASCADE,
        related_name='login_credentials',
    )
    user_id = models.CharField(max_length=10, db_column='user_id')
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    auth_ulid = models.ForeignKey(
        Authentication,
        db_column='auth_ulid',
        to_field='id',
        on_delete=models.CASCADE,
        related_name='login_credentials',
    )
    enable_flag = models.BooleanField(default=True)
    biometric_info = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Login_Credential'
        managed = False
