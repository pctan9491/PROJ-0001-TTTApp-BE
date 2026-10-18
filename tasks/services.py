from dataclasses import dataclass
from django.db import IntegrityError, transaction
from tasks.models import Task, SubTask
from accounts.models import Users
from datetime import datetime

class TaskCreationError(Exception):
    pass


def create_task(
    *,
    task_id: str,
    task_title: str,
    task_detail: str,
    task_status: str,
    priority_level: str,
    schedule,
    user_ulid: str,
    user_id: str,
    eisenhower_matrix_uuid: str,
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
                user_ulid=user_ulid,
                user_id=user_id,
                eisenhower_matrix_uuid=eisenhower_matrix_uuid,
                created_at=datetime.now(),
            )

            return task
    except IntegrityError as exc:
        raise TaskCreationError('Task Creation Failed') from exc

def get_task (
    *,
    user: Users,
    filters: dict,
):
    with transaction.atomic():
        #1 Get all tasks from login user
        tasks = Task.objects.filter(user_ulid=user.user_ulid, **filters)

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
