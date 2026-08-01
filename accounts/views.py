from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import issue_token
from accounts.serializers import LoginSerializer, RegisterSerializer
from accounts.services import LoginError, RegistrationError, login_user, register_user


def _user_payload(user):
    return {
        'id': str(user.id),
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'birth_date': user.birth_date.isoformat(),
    }


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = register_user(**serializer.validated_data)
        except RegistrationError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        token = issue_token(user=result.user)
        return Response(
            {'access_token': token, 'user': _user_payload(result.user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = login_user(**serializer.validated_data)
        except LoginError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        token = issue_token(user=result.user)
        return Response({'access_token': token, 'user': _user_payload(result.user)})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'user': _user_payload(user)})
