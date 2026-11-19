import React from "react";
import type { Task, TaskStatus } from "../types/task";

interface TaskListProps {
  readonly tasks: readonly Task[];
  readonly isLoading?: boolean;
  readonly onStatusChange?: (taskId: string, newStatus: TaskStatus) => void;
  readonly emptyMessage?: string;
}

const statusLabels: Record<TaskStatus, string> = {
  todo: "À faire",
  in_progress: "En cours",
  done: "Terminée",
  cancelled: "Annulée",
};

const statusColors: Record<TaskStatus, string> = {
  todo: "bg-slate-100 text-slate-800",
  in_progress: "bg-blue-100 text-blue-800",
  done: "bg-emerald-100 text-emerald-800",
  cancelled: "bg-rose-100 text-rose-800",
};

/**
 * Composant d'interface isolé, purement présentationnel.
 * - Typage strict (props en readonly, pas de any)
 * - Accessibilité de base (role, aria)
 * - Styles Tailwind uniquement (aucune CSS custom)
 * - Aucune logique métier : les transitions sont déléguées au parent / service
 */
export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  isLoading = false,
  onStatusChange,
  emptyMessage = "Aucune tâche pour le moment.",
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8 text-slate-500" role="status">
        Chargement des tâches…
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-slate-300 p-8 text-center text-slate-500">
        {emptyMessage}
      </div>
    );
  }

  return (
    <ul className="space-y-3" role="list">
      {tasks.map((task) => (
        <li
          key={task.id}
          className="flex items-start justify-between rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md"
        >
          <div className="min-w-0 flex-1">
            <h3 className="truncate text-base font-semibold text-slate-900">{task.title}</h3>
            {task.description && (
              <p className="mt-1 line-clamp-2 text-sm text-slate-600">{task.description}</p>
            )}
            <div className="mt-2 flex items-center gap-2">
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${statusColors[task.status]}`}
              >
                {statusLabels[task.status]}
              </span>
              <span className="text-xs text-slate-400">Priorité : {task.priority}</span>
            </div>
          </div>

          {onStatusChange && task.status !== "done" && task.status !== "cancelled" && (
            <button
              type="button"
              onClick={() =>
                onStatusChange(
                  task.id,
                  task.status === "todo" ? "in_progress" : "done",
                )
              }
              className="ml-4 shrink-0 rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
              aria-label={`Avancer la tâche ${task.title}`}
            >
              {task.status === "todo" ? "Démarrer" : "Terminer"}
            </button>
          )}
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
