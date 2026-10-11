from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def post (self, request):
        #Serializer
        return Response(
            {
                "message": "Task created successfully"
            },
            status = status.HTTP_201_CREATED
        )

class ViewTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        #Serializer
        return Response(
            {
                "message": "Task view successfully"
            },
            status = status.HTTP_200_OK
        )




