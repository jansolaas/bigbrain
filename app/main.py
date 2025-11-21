from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.api.v1 import router as api_v1_router

# Import models so that Base knows about them before create_all
from app.models import Asset, Project, Shot, Version, tasks, users

from app.core.seed import seed_dev_data

# Create database tables
Base.metadata.create_all(bind=engine)
# Seed dev data if DB is empty
with SessionLocal() as db:
    seed_dev_data(db)

app = FastAPI(title="BigBrain Pipeline API")

# Include all v1 routes under /api/v1
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "BigBrain API is running 🚀"}