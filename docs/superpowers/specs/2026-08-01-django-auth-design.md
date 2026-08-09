# Django Auth (Register/Login) Design

**Goal**

Build password-based registration and login in a new Django backend connected to an existing PostgreSQL database schema (`Users`, `Login_Credential`, `Authentication`). Provide JSON REST APIs that can be tested with SOAP UI and later consumed by a Dart client.

## Scope

In scope:

- Register a new user using `Authentication` row for password (`/oauth/password/callback`)
- Login with `username` or `email` + password
- Return an access token (signed opaque token) and basic user payload
- Optional: `/api/auth/me/` to validate token and fetch current user

Out of scope (next phase):

- Google OAuth callback flow
- Email verification and password reset
- Biometric login
- Refresh tokens and revocation management

## Data Model (Existing Tables)

Backend uses existing tables created in PostgreSQL:

- `Users`
  - `id` UUID primary key
  - `user_id` varchar(10) unique
  - `first_name`, `last_name`, `gender`, `birth_date`
  - `created_at`
- `Login_Credential`
  - `id` UUID primary key
  - `user_ulid` UUID references `Users(id)`
  - `user_id` varchar(10) references `Users(user_id)`
  - `username` unique
  - `email` unique
  - `password_hash` string
  - `auth_ulid` UUID references `Authentication(id)`
  - `enable_flag` boolean
  - `biometric_info` string optional
  - `created_at`
- `Authentication`
  - `id` UUID primary key
  - `auth_path` string (includes `/oauth/password/callback`)

Django models map to these tables with `db_table` and `managed = False` (so Django will not attempt to create/alter them).

## Auth Token Design

For initial implementation, access token is an opaque signed string produced by Django signing utilities:

- Issue token via `django.core.signing.dumps(payload, salt=...)`
- Verify token via `django.core.signing.loads(token, salt=..., max_age=...)`

This avoids introducing JWT dependencies and does not require Django’s built-in `auth_user` table. Token is treated as a Bearer token by the API.

## API Design

Base path: `/api/auth`

### Register

- `POST /api/auth/register/`
- Request JSON:
  - `user_id`, `first_name`, `last_name`, `gender`, `birth_date`
  - `username`, `email`, `password`
- Behavior:
  - Validate uniqueness: `Users.user_id`, `Login_Credential.username`, `Login_Credential.email`
  - Find `Authentication.id` where `auth_path = '/oauth/password/callback'`
  - Insert `Users`
  - Insert `Login_Credential` with `password_hash = make_password(password)`
- Response JSON:
  - `access_token`
  - `user` object (id, user_id, first_name, last_name, gender, birth_date)

### Login

- `POST /api/auth/login/`
- Request JSON:
  - `login` (username or email)
  - `password`
- Behavior:
  - Find `Login_Credential` by `username = login OR email = login`
  - Check `enable_flag = true`
  - Verify password with `check_password(password, password_hash)`
  - Return token + user payload
- Response JSON:
  - `access_token`
  - `user` object

### Me (Optional)

- `GET /api/auth/me/`
- Header:
  - `Authorization: Bearer <access_token>`
- Response JSON:
  - `user` object

## Error Handling

- Validation errors return HTTP 400 with field-level messages
- Invalid credentials return HTTP 401
- Missing/invalid token returns HTTP 401
- Database integrity collisions (unique constraints) return HTTP 400 with a clear error message

## Security

- Never store raw password; store only `make_password` output
- Do not log passwords or returned tokens
- Use environment variables for DB credentials and Django secret key

