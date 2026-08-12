from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicle_router

# Importing User registers the model with SQLAlchemy.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Logistics & Fleet Management System",
    description="Logistics and Fleet Management REST API",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(vehicle_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Logistics & Fleet Management System API",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
    }