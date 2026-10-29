from dataclasses import dataclass
from django.db import IntegrityError, transaction
from tasks.models import Task, SubTask, EisenhowerMatrix
from accounts.models import Users
from django.utils import timezone

class TaskCreationError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass

def create_task(
    *,
    user: Users,
    task_id: str,
    task_title: str,
    task_detail: str,
    task_status: str,
    priority_level: str,
    schedule,
    eisenhower_matrix_id: str,
) -> Task:

    try:
        with transaction.atomic():
            task = Task.objects.create(
                task_id=task_id,
                task_title=task_title,
                task_detail=task_detail,
                task_status=task_status,
                priority_level=priority_level,
                schedule=schedule,
                user_ulid=user,
                user_id=user.user_id,
                eisenhower_matrix_uuid=EisenhowerMatrix.objects.get( eisenhower_matrix_id=eisenhower_matrix_id),
                created_at=timezone.now(),
            )

            return task
    except IntegrityError as exc:
        raise TaskCreationError('Task Creation Failed') from exc

def get_task (
    *,
    user: Users,
    filters: dict,
):
    try:
        with transaction.atomic():
            #1 Get all tasks from login user
            tasks = Task.objects.filter(user_ulid=user, **filters)

            #2 Filter by any field
            if filters.get("task_id"):
                tasks = tasks.filter(task_id=filters["task_id"])
            if filters.get("task_title"):
                tasks = tasks.filter(task_title__contains=filters["task_title"])
            if filters.get("task_status"):
                tasks = tasks.filter(task_status=filters["task_status"])
            if filters.get("priority_level"):
                tasks = tasks.filter(priority_level=filters["priority_level"])
            if filters.get("schedule"):
                tasks = tasks.filter(schedule=filters["schedule"])
            if filters.get("eisenhower_matrix_uuid"):
                tasks = tasks.filter(eisenhower_matrix_uuid=filters["eisenhower_matrix_uuid"])

            #3 Return tasks sorted by created_at with filtered condition(s) (if any)
            return tasks.order_by('created_at')
    except Task.DoesNotExist:
        raise TaskNotFoundError('Task not found')

def create_sub_task(
    *,
    user: Users,
    sub_task_id: str,
    sub_task_title: str,
    sub_task_description: str,
    sub_task_status: str,
    sub_task_schedule,
    sub_task_priority: str,
    task_id: str,
) -> SubTask:

    try:
        with transaction.atomic():
            sub_task = SubTask.objects.create(
                sub_task_id=sub_task_id,
                sub_task_title=sub_task_title,
                sub_task_description=sub_task_description,
                sub_task_status=sub_task_status,
                sub_task_schedule=sub_task_schedule,
                sub_task_priority=sub_task_priority,
                task_ulid=Task.objects.get(task_id=task_id, user_ulid=user),
                created_at=timezone.now(),
            )
            return sub_task
    except IntegrityError as exc:
        raise TaskCreationError('Sub Task Creation Failed') from exc

def get_sub_task(
    *,
    user: Users,
    task_id: str,
    filters: dict,
):
    try:
        with transaction.atomic():
            #1 Get all sub tasks from login user and main task_id
            parent_task = Task.objects.get(task_id=task_id, user_ulid=user)
            sub_tasks = SubTask.objects.filter(task_ulid=parent_task)

            #2 Filter by any field
            if filters.get("sub_task_id"):
                sub_tasks = sub_tasks.filter(sub_task_id=filters["sub_task_id"])
            if filters.get("sub_task_title"):
                sub_tasks = sub_tasks.filter(sub_task_title__contains=filters["sub_task_title"])
            if filters.get("sub_task_status"):
                sub_tasks = sub_tasks.filter(sub_task_status=filters["sub_task_status"])
            if filters.get("sub_task_schedule"):
                sub_tasks = sub_tasks.filter(sub_task_schedule=filters["sub_task_schedule"])
            if filters.get("sub_task_priority"):
                sub_tasks = sub_tasks.filter(sub_task_priority=filters["sub_task_priority"])
            
            #3 Return sub tasks sorted by created_at
            return sub_tasks.order_by('created_at')
    except SubTask.DoesNotExist:
        raise TaskNotFoundError('Sub Task not found')


    
