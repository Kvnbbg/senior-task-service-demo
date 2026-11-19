from fastapi import FastAPI

from app.routers.task_router import router as task_router

app = FastAPI(
    title="Senior Task Service",
    description="API de gestion de tâches avec typage strict, modèles étanches et logique métier isolée.",
    version="1.0.0",
)

app.include_router(task_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
