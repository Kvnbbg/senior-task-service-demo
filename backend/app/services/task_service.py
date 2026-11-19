from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.task import Task, TaskCreate, TaskStatus, TaskUpdate


class TaskNotFoundError(Exception):
    """Erreur métier : tâche inexistante."""


class InvalidStatusTransitionError(Exception):
    """Erreur métier : transition de statut interdite."""


class TaskService:
    """
    Service métier isolé.
    Toute la logique de validation métier et de transition d'état vit ici.
    Aucune dépendance directe à FastAPI ou à la persistance (ici in-memory pour l'exemple).
    """

    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def create_task(self, payload: TaskCreate) -> Task:
        """Crée une tâche avec validation stricte via le modèle."""
        task = Task(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: UUID) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Tâche {task_id} introuvable")
        return task

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority.value == priority]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> Task:
        existing = self.get_task(task_id)

        # Règle métier : on ne peut pas repasser une tâche DONE ou CANCELLED en TODO
        if payload.status is not None:
            self._validate_status_transition(existing.status, payload.status)

        # Reconstruction immuable (puisque frozen)
        update_data = payload.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_data)
        # Force la mise à jour du timestamp
        updated = updated.model_copy(update={"updated_at": datetime.utcnow()})

        self._tasks[task_id] = updated
        return updated

    def _validate_status_transition(self, current: TaskStatus, new: TaskStatus) -> None:
        """Transitions autorisées uniquement dans le sens de progression ou annulation contrôlée."""
        allowed = {
            TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
            TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.CANCELLED, TaskStatus.TODO},
            TaskStatus.DONE: set(),  # Terminal
            TaskStatus.CANCELLED: set(),  # Terminal
        }
        if new not in allowed.get(current, set()) and new != current:
            raise InvalidStatusTransitionError(
                f"Transition interdite : {current.value} → {new.value}"
            )
