/**
 * Modèles de données étanches côté client.
 * Miroir strict des modèles Pydantic du backend.
 * Aucun `any`, aucun champ optionnel non documenté.
 */

export const TaskStatus = {
  TODO: "todo",
  IN_PROGRESS: "in_progress",
  DONE: "done",
  CANCELLED: "cancelled",
} as const;

export type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus];

export const TaskPriority = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
} as const;

export type TaskPriority = (typeof TaskPriority)[keyof typeof TaskPriority];

export interface Task {
  readonly id: string;
  readonly title: string;
  readonly description: string | null;
  readonly priority: TaskPriority;
  readonly status: TaskStatus;
  readonly created_at: string; // ISO 8601
  readonly updated_at: string;
}

export interface TaskCreatePayload {
  readonly title: string;
  readonly description?: string | null;
  readonly priority?: TaskPriority;
  readonly status?: TaskStatus;
}

export interface TaskUpdatePayload {
  readonly title?: string;
  readonly description?: string | null;
  readonly priority?: TaskPriority;
  readonly status?: TaskStatus;
}
