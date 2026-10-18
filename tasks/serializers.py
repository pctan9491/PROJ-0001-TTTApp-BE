from rest_framework import serializers
from tasks.models import Task, EisenhowerMatrix

class CreateTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=10)
    task_title = serializers.CharField(max_length=70)
    task_detail = serializers.CharField(max_length=500)
    task_status = serializers.CharField(max_length=10)
    priority_level = serializers.CharField(max_length=10)
    schedule = serializers.DateField()
    eisenhower_matrix_id = serializers.CharField(max_length=10)

class ViewTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=10, required=False)
    task_title = serializers.CharField(max_length=70, required=False)
    task_status = serializers.CharField(max_length=10, required=False)
    priority_level = serializers.CharField(max_length=10, required=False)
    eisenhower_matrix_id = serializers.CharField(max_length=10, required=False)