from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Shot, Project
from app.schemas.shot import ShotOut, ShotCreate

router = APIRouter(prefix="/shots", tags=["shots"])


@router.get("/", response_model=List[ShotOut])
def list_shots(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List shots, optionally filtered by project_id."""
    query = db.query(Shot)
    if project_id is not None:
        query = query.filter(Shot.project_id == project_id)
    return query.all()


@router.post("/", response_model=ShotOut, status_code=201)
def create_shot(payload: ShotCreate, db: Session = Depends(get_db)):
    """Create a new shot for a project."""
    # Ensure project exists
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if project is None:
        raise HTTPException(status_code=400, detail="Project does not exist")

    # Optional: enforce unique shot name within project
    existing = (
        db.query(Shot)
        .filter(Shot.project_id == payload.project_id, Shot.name == payload.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Shot with this name already exists in this project",
        )

    shot = Shot(
        project_id=payload.project_id,
        name=payload.name,
        sequence=payload.sequence,
        frame_start=payload.frame_start,
        frame_end=payload.frame_end,
        fps=payload.fps,
    )

    db.add(shot)
    db.commit()
    db.refresh(shot)

    return shot