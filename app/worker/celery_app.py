from app.core.config import settings
from app.db.database import SessionLocal
from app.services.inventory import InventoryService

celery_app = Celery("worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def cleanup_expired_reservations_task():
    db = SessionLocal()
    try:
        count = InventoryService.cleanup_expired_reservations(db)
        return f"Cleaned up {count} expired reservations"
    finally:
        db.close()

# Configure periodic task
celery_app.conf.beat_schedule = {
    "cleanup-every-minute": {
        "task": "app.worker.celery_app.cleanup_expired_reservations_task",
        "schedule": 60.0,
    },
}
