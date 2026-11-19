from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskBase(BaseModel):
    model_config = ConfigDict(
        frozen=True,  # Modèle étanche : immuable après création
        extra="forbid",  # Refuse les champs inconnus
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    title: str = Field(..., min_length=3, max_length=200, description="Titre de la tâche")
    description: Optional[str] = Field(None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty_after_strip(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Le titre ne peut pas être vide ou composé uniquement d'espaces")
        return v


class TaskCreate(TaskBase):
    """Modèle d'entrée pour création. Pas d'id ni de timestamps."""


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    """Modèle complet, étanche, avec identifiants et métadonnées."""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        from_attributes=True,
    )
