from fastapi import FastAPI
from app.database import Base, engine
from app.api.v1 import router as api_v1_router

# Import models so that Base knows about them before create_all
from app.models import Asset, Project, Shot

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BigBrain Pipeline API")

# Include all v1 routes under /api/v1
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "BigBrain API is running 🚀"}