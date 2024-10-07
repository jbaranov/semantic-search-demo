from celery import Celery

from app.core.config import settings

# Create a Celery instance
celery_app = Celery("worker", config_source=settings.celery)

# Auto-discover tasks in the specified packages
celery_app.autodiscover_tasks(["app.worker.tasks"])
