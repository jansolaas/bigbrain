from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Project
from app.schemas.project import ProjectOut, ProjectCreate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    """List all projects."""
    projects = db.query(Project).all()
    return projects


@router.post("/", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    # Ensure name/code are unique
    existing_by_name = db.query(Project).filter(Project.name == payload.name).first()
    if existing_by_name:
        raise HTTPException(status_code=400, detail="Project with this name already exists")

    existing_by_code = db.query(Project).filter(Project.code == payload.code).first()
    if existing_by_code:
        raise HTTPException(status_code=400, detail="Project with this code already exists")

    project = Project(
        name=payload.name,
        code=payload.code,
        root_path=payload.root_path,
        description=payload.description,
        is_active=payload.is_active,
        fps=payload.fps,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project