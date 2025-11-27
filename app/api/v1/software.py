from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Software
from app.schemas.software import SoftwareOut, SoftwareCreate

router = APIRouter(prefix="/software", tags=["software"])


@router.get("/", response_model=List[SoftwareOut])
def list_software(
        name: Optional[str] = None,
        active_only: bool = False,
        db: Session = Depends(get_db)
):
    query = db.query(Software)
    if name:
        query = query.filter(Software.name == name)
    if active_only:
        query = query.filter(Software.is_active == True)
    return query.all()


@router.post("/", response_model=SoftwareOut)
def create_software(payload: SoftwareCreate, db: Session = Depends(get_db)):
    # Check duplicate
    existing = db.query(Software).filter(
        Software.name == payload.name,
        Software.version == payload.version
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Software version already exists")

    soft = Software(**payload.model_dump())
    db.add(soft)
    db.commit()
    db.refresh(soft)
    return soft