# Senior Task Service Demo

Démonstration de **rigueur architecturale senior** face au code jetable des « vibe coders ».

## Objectif

Livrer une **brique fonctionnelle isolée** (service API + composant d'interface) avec :

- Typage strict et modèles de données étanches
- Logique métier séparée des couches d'interface
- Tests unitaires systématiques (100 % de succès obligatoire)
- Documentation de niveau Pull Request senior

## Stack

- **Backend** : Python 3.10+, FastAPI, Pydantic v2
- **Frontend** : TypeScript, React, Tailwind CSS
- **Tests** : Pytest

## Architecture

```
backend/
├── app/
│   ├── models/task.py          # Modèles Pydantic étanches (frozen, extra=forbid)
│   ├── services/task_service.py # Logique métier pure + règles de transition
│   ├── routers/task_router.py   # Couche HTTP uniquement
│   └── main.py
└── tests/
    └── test_task_service.py     # 8 tests, 100 % passés

frontend/
└── src/
    ├── types/task.ts            # Types miroir stricts (readonly)
    └── components/TaskList.tsx  # Composant présentationnel isolé
```

### Choix techniques

1. **Modèles immuables** (`frozen=True`) : impossible de muter accidentellement un objet métier.
2. **Validation stricte** à l'entrée (min_length, enum, field_validator).
3. **Service isolé** : aucune dépendance à FastAPI ou à une base. Facilement testable et remplaçable par une implémentation DB.
4. **Transitions d'état explicites** : machine à états simple pour éviter les états incohérents.
5. **Composant React purement présentationnel** : props en `readonly`, pas de logique métier, styles Tailwind only.

## Exécution des tests

```bash
cd backend
PYTHONPATH=. pytest -v
```

Résultat (19 novembre 2026) :

```
============================= test session starts ==============================
collected 8 items

tests/test_task_service.py::test_create_task_happy_path PASSED
tests/test_task_service.py::test_create_task_rejects_short_title PASSED
tests/test_task_service.py::test_create_task_rejects_whitespace_only_title PASSED
tests/test_task_service.py::test_get_task_not_found PASSED
tests/test_task_service.py::test_update_task_status_transition_allowed PASSED
tests/test_task_service.py::test_update_task_status_transition_forbidden PASSED
tests/test_task_service.py::test_list_tasks_filters_by_status PASSED
tests/test_task_service.py::test_task_model_is_frozen PASSED

============================== 8 passed in 4.32s ===============================
```

**100 % de succès. Aucun commit n'a été effectué avant ce résultat.**

## Lancement de l'API

```bash
cd backend
uvicorn app.main:app --reload
```

Endpoints disponibles sous `/api/v1/tasks`.

---

*Ce dépôt a été produit dans le cadre d'un exercice de démonstration de standards senior.*
