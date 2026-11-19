from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.task import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.services.task_service import (
    InvalidStatusTransitionError,
    TaskNotFoundError,
    TaskService,
)


@pytest.fixture
def service() -> TaskService:
    return TaskService()


def test_create_task_happy_path(service: TaskService) -> None:
    payload = TaskCreate(
        title="Écrire les tests unitaires",
        description="Couverture 100 % obligatoire",
        priority=TaskPriority.HIGH,
    )
    task = service.create_task(payload)

    assert isinstance(task.id, UUID)
    assert task.title == "Écrire les tests unitaires"
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.HIGH
    assert isinstance(task.created_at, datetime)


def test_create_task_rejects_short_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="ab")


def test_create_task_rejects_whitespace_only_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_get_task_not_found(service: TaskService) -> None:
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    with pytest.raises(TaskNotFoundError):
        service.get_task(fake_id)


def test_update_task_status_transition_allowed(service: TaskService) -> None:
    created = service.create_task(TaskCreate(title="Tâche de test"))
    updated = service.update_task(
        created.id,
        TaskUpdate(status=TaskStatus.IN_PROGRESS),
    )
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.updated_at >= created.updated_at


def test_update_task_status_transition_forbidden(service: TaskService) -> None:
    created = service.create_task(TaskCreate(title="Tâche terminée"))
    # Passer d'abord en IN_PROGRESS puis DONE
    in_progress = service.update_task(created.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
    done = service.update_task(in_progress.id, TaskUpdate(status=TaskStatus.DONE))
    # Essayer de revenir en TODO → interdit
    with pytest.raises(InvalidStatusTransitionError):
        service.update_task(done.id, TaskUpdate(status=TaskStatus.TODO))


def test_list_tasks_filters_by_status(service: TaskService) -> None:
    service.create_task(TaskCreate(title="À faire 1"))
    t2 = service.create_task(TaskCreate(title="En cours"))
    service.update_task(t2.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
    service.create_task(TaskCreate(title="À faire 2"))

    todos = service.list_tasks(status=TaskStatus.TODO)
    in_progress = service.list_tasks(status=TaskStatus.IN_PROGRESS)

    assert len(todos) == 2
    assert len(in_progress) == 1
    assert all(t.status == TaskStatus.TODO for t in todos)


def test_task_model_is_frozen() -> None:
    task = Task(title="Immutable")
    with pytest.raises(ValidationError):
        task.title = "Tentative de mutation"  # type: ignore[misc]
