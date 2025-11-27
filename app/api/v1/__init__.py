from fastapi import APIRouter
from app.api.v1 import assets, projects, shots, versions, sequences, tasks, users, software

router = APIRouter()
router.include_router(assets.router)
router.include_router(projects.router)
router.include_router(sequences.router)
router.include_router(shots.router)
router.include_router(versions.router)
router.include_router(tasks.router)
router.include_router(users.router)
router.include_router(software.router)