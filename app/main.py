from app.core.config import settings
from app.api.v1.api import api_router
from app.db.database import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A sophisticated backend service for real-time inventory tracking and dynamic pricing.",
    version=settings.VERSION,
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Inventory and Dynamic Pricing API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
