from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class CreateTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['Tasks'],
        summary='Create a new task',
        request="pending",
        responses={201: OpenApiTypes.OBJECT},
        auth=[],
    )
    def post (self, request):
        #Serializer
        return Response(
            {
                "message": "Task created successfully"
            },
            status = status.HTTP_201_CREATED
        )

class ViewTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=['Tasks'],
        summary='View user tasks',
        description='Retrieve specific user tasks',
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        #Serializer
        return Response(
            {
                "message": "Task view successfully"
            },
            status = status.HTTP_200_OK
        )




