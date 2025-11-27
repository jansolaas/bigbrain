from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Sequence, Project, Episode
from app.schemas.sequence import SequenceOut, SequenceCreate

router = APIRouter(prefix="/sequences", tags=["sequences"])


@router.get("/", response_model=List[SequenceOut])
def list_sequences(
        project_id: Optional[int] = None,
        episode_id: Optional[int] = None,
        active_only: bool = True,  # New default
        db: Session = Depends(get_db),
):
    query = db.query(Sequence)
    if project_id:
        query = query.filter(Sequence.project_id == project_id)
    # ... existing filters ...

    if active_only:
        query = query.filter(Sequence.is_active == True)

    return query.all()


@router.post("/", response_model=SequenceOut, status_code=201)
def create_sequence(payload: SequenceCreate, db: Session = Depends(get_db)):
    """Create a new sequence."""
    # Validate project
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    # Validate episode if provided
    if payload.episode_id is not None:
        episode = db.query(Episode).filter(Episode.id == payload.episode_id).first()
        if not episode:
            raise HTTPException(status_code=400, detail="Episode not found")
        # Ensure episode belongs to same project
        if episode.project_id != payload.project_id:
            raise HTTPException(status_code=400, detail="Episode project mismatch")

    # Check uniqueness (name within project+episode)
    existing = (
        db.query(Sequence)
        .filter(
            Sequence.project_id == payload.project_id,
            Sequence.episode_id == payload.episode_id,
            Sequence.name == payload.name
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Sequence name already exists in this context")

    sequence = Sequence(
        project_id=payload.project_id,
        episode_id=payload.episode_id,
        name=payload.name,
        description=payload.description,
    )
    db.add(sequence)
    db.commit()
    db.refresh(sequence)
    return sequence