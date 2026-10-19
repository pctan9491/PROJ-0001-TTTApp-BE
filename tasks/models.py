from django.db import models
from tasks.uuidv7 import uuidv7


class EisenhowerMatrix(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    eisenhower_matrix_id = models.CharField(max_length=10)
    eisenhower_matrix_options = models.CharField(max_length=20)

    class Meta:
        db_table = 'eisenhower_matrix'
        managed = False

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    task_id = models.CharField(max_length=10, unique=True)
    task_title = models.CharField(max_length=70)
    task_detail = models.TextField()
    task_status = models.CharField(max_length=10)
    priority_level = models.CharField(max_length=10)
    schedule = models.DateField()
    user_ulid = models.ForeignKey(
        Users,
        db_column='user_ulid',
        to_field='id',
        on_delete=models.CASCADE,
        related_name='task',
    )
    user_id = models.CharField(max_length=10, db_column='user_id')
    eisenhower_matrix_uuid = models.ForeignKey(
        EisenhowerMatrix,
        db_column='eisenhower_matrix_uuid',
        to_field='id',
        on_delete=models.CASCADE,
        related_name='task',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task'
        managed = False

class SubTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuidv7, editable=False)
    sub_task_id = models.CharField(max_length=10, unique=True)
    sub_task_title = models.CharField(max_length=70)
    sub_task_description = models.TextField()
    sub_task_status = models.CharField(max_length=10)
    sub_task_schedule = models.DateField()
    sub_task_priority = models.CharField(max_length=10)
    task_ulid = models.ForeignKey(
        Task,
        db_column='task_ulid',
        to_field='id',
        on_delete=models.CASCADE,
        related_name='sub_task',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sub_task'
        managed = False