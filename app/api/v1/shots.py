from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Shot, Project
from app.schemas.shot import ShotOut, ShotCreate

from app.core.fps import resolve_fps_for_shot

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

@router.get("/{shot_id}", response_model=ShotOut)
def get_shot(shot_id: int, db: Session = Depends(get_db)):
    """Get a single shot by ID."""
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if shot is None:
        raise HTTPException(status_code=404, detail="Shot not found")
    return shot

@router.post("/", response_model=ShotOut, status_code=201)
def create_shot(payload: ShotCreate, db: Session = Depends(get_db)):
    """Create a new shot for a project."""
    # Ensure project exists
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if project is None:
        raise HTTPException(status_code=400, detail="Project does not exist")

    # If sequence_id is provided, ensure it exists and belongs to the same project
    if payload.sequence_id is not None:
        sequence = db.query(Sequence).filter(Sequence.id == payload.sequence_id).first()
        if sequence is None:
            raise HTTPException(status_code=400, detail="Sequence does not exist")
        if sequence.project_id != payload.project_id:
            raise HTTPException(
                status_code=400,
                detail="Sequence does not belong to the same project",
            )

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
        sequence_id=payload.sequence_id,
        name=payload.name,
        frame_start=payload.frame_start,
        frame_end=payload.frame_end,
        fps=payload.fps,
    )

    db.add(shot)
    db.commit()
    db.refresh(shot)

    return shot

@router.get("/{shot_id}/fps", response_model=float)
def get_shot_fps(shot_id: int, db: Session = Depends(get_db)):
    """
    Get the effective fps for a shot, resolving overrides.
    """
    try:
        fps = resolve_fps_for_shot(db, shot_id=shot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return fps