from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from accounts.models import Users
from tasks.serializers import CreateTaskSerializer, ViewTaskSerializer, CreateSubTaskSerializer, ViewSubTaskSerializer, ViewSubTaskSerializer
from tasks.services import TaskCreationError, TaskNotFoundError, create_task, get_task, create_sub_task, get_sub_task

def _user_payload(user):
    return {
        'id': str(user.id),
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
        'eisenhower_matrix_uuid': str(task.eisenhower_matrix_uuid_id),
        'created_at': task.created_at.isoformat(),
    }

def _sub_task_payload(sub_task):
    return{
        'sub_task_ulid': str(sub_task.id),
        'sub_task_id': sub_task.sub_task_id,
        'sub_task_title': sub_task.sub_task_title,
        'sub_task_description': sub_task.sub_task_description,
        'sub_task_status': sub_task.sub_task_status,
        'sub_task_schedule': sub_task.sub_task_schedule.isoformat(),
        'sub_task_priority': sub_task.sub_task_priority,
        'task_ulid': str(sub_task.task_ulid),
        'created_at': sub_task.created_at.isoformat(),
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
    def post(self, request):
        #Serializer
        serializer = ViewTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tasks = get_task(user=request.user, filters=serializer.validated_data)

            #Convert each Task into a Dictionary
            task_payload = [_task_payload(task) for task in tasks ]
            return Response(
                {
                    'task':task_payload,
                    'user': _user_payload(request.user)
                },
                status=status.HTTP_200_OK
            )
        except TaskNotFoundError as exc:
            return Response({'Details': str(exc)}, status=status.HTTP_404_NOT_FOUND)

class CreateSubTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['SubTasks'],
        summary='Create a new sub task',
        request=CreateSubTaskSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        #Serializer
        serializer = CreateSubTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sub_task = create_sub_task(user=request.user, **serializer.validated_data)
        except TaskCreationError as exc:
            return Response({'detail':str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'sub_task': _sub_task_payload(sub_task),
                'task': _task_payload(sub_task.task_ulid),
                'user': _user_payload(request.user)
            },
            status = status.HTTP_201_CREATED
        )

class ViewSubTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['SubTasks'],
        summary='View user sub tasks based on main task',
        request=ViewSubTaskSerializer,
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        #Serializer
        serializer = ViewSubTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sub_tasks = get_sub_task(task_id=serializer.validated_data["task_id"], user=request.user, 
            filters=serializer.validated_data)

            #Convert each SubTask into a Dictionary
            sub_task_payload = [_sub_task_payload(sub_task) for sub_task in sub_tasks]
            return Response(
                {
                    'sub_task': sub_task_payload,
                    'task': _task_payload(sub_tasks[0].task_ulid),
                    'user': _user_payload(request.user)
                },
                status=status.HTTP_200_OK
            )
        except TaskNotFoundError as exc:
            return Response({'Details': str(exc)}, status=status.HTTP_404_NOT_FOUND)






