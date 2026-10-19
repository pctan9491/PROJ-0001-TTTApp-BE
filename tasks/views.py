from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from accounts.models import Users
from tasks.serializers import CreateTaskSerializer, ViewTaskSerializer
from tasks.services import TaskCreationError, TaskNotFoundError, create_task, get_task

def _user_payload(user):
    return {
        'user_ulid': str(user.id),
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'birth_date': user.birth_date.isoformat(),
    }

def _task_payload(task):
    return{
        'task_ulid': str(task.id),
        'task_id': task.task_id,
        'task_title': task.task_title,
        'task_detail': task.task_detail,
        'task_status': task.task_status,
        'priority_level': task.priority_level,
        'schedule': task.schedule.isoformat(),
        'user_ulid': str(task.user_ulid),
        'user_id': task.user_id,
        'eisenhower_matrix_uuid': task.eisenhower_matrix_uuid,
        'created_at': task.created_at.isoformat(),
    }

class CreateTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['Tasks'],
        summary='Create a new task',
        request=CreateTaskSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def post (self, request):
        #Serializer
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            task = create_task(user=request.user, **serializer.validated_data)
        except TaskCreationError as exc:
            return Response({'detail':str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'access_token': request.user.access_token,
                'task': _task_payload(task),
                'user': _user_payload(request.user)
            },
            status = status.HTTP_201_CREATED
        )

class ViewTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=['Tasks'],
        summary='View user tasks',
        description='Retrieve specific user tasks',
        request=ViewTaskSerializer,
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        #Serializer
        serializer = ViewTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            task = get_task(**serializer.validated_data)
            return Response(
                {
                    'access_token': request.user.access_token,
                    'task': _task_payload(task),
                    'user': _user_payload(request.user)
                },
                status=status.HTTP_200_OK
            )
        except TaskNotFoundError as exc:
            return Response({'Details': str(exc)}, status=status.HTTP_404_NOT_FOUND)




