from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Shot, Project
from app.schemas.shot import ShotOut, ShotCreate, ShotUpdate
from app.models import Sequence
from app.core.fps import resolve_fps_for_shot

router = APIRouter(prefix="/shots", tags=["shots"])


@router.get("/", response_model=List[ShotOut])
def list_shots(
        project_id: Optional[int] = None,
        sequence_id: Optional[int] = None,
        active_only: bool = True,  # New default filter
        db: Session = Depends(get_db),
):
    query = db.query(Shot)
    if project_id:
        query = query.filter(Shot.project_id == project_id)
    if sequence_id:
        query = query.filter(Shot.sequence_id == sequence_id)

    # Filter logic
    if active_only:
        query = query.filter(Shot.is_active == True)

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

    # Ensure sequence exists and belongs to project
    sequence = db.query(Sequence).filter(Sequence.id == payload.sequence_id).first()
    if sequence is None:
        raise HTTPException(status_code=400, detail="Sequence does not exist")

    if sequence.project_id != payload.project_id:
        raise HTTPException(
            status_code=400,
            detail="Sequence does not belong to the same project",
        )

    # Enforce unique shot name
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


@router.patch("/{shot_id}", response_model=ShotOut)
def update_shot(
        shot_id: int,
        payload: ShotUpdate,
        db: Session = Depends(get_db)
):
    """Update a shot (e.g. rename, omit, change frames)."""
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")

    # Python magic to update only the fields sent in payload
    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(shot, key, value)

    db.add(shot)
    db.commit()
    db.refresh(shot)
    return shot