from fastapi import APIRouter
from app.api.v1 import assets, projects, shots

router = APIRouter()
router.include_router(assets.router)
router.include_router(projects.router)
router.include_router(shots.router)