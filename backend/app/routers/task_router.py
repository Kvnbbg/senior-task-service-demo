from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.task import Task, TaskCreate, TaskStatus, TaskUpdate
from app.services.task_service import (
    InvalidStatusTransitionError,
    TaskNotFoundError,
    TaskService,
)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

# Instance partagée pour la démo (en production : dependency injection + DB)
_service = TaskService()


def get_task_service() -> TaskService:
    return _service


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une tâche",
)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    return service.create_task(payload)


@router.get(
    "",
    response_model=List[Task],
    summary="Lister les tâches",
)
def list_tasks(
    status_filter: Optional[TaskStatus] = None,
    service: TaskService = Depends(get_task_service),
) -> List[Task]:
    return service.list_tasks(status=status_filter)


@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Récupérer une tâche",
)
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> Task:
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.patch(
    "/{task_id}",
    response_model=Task,
    summary="Mettre à jour une tâche",
)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    try:
        return service.update_task(task_id, payload)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidStatusTransitionError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
