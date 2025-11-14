from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Asset, Project
from app.schemas.asset import AssetOut, AssetCreate

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=List[AssetOut])
def get_assets(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List all assets, optionally filtered by project_id."""
    query = db.query(Asset)
    if project_id is not None:
        query = query.filter(Asset.project_id == project_id)
    return query.all()


@router.post("/", response_model=AssetOut, status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    """Create a new asset."""

    # Ensure project exists
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if project is None:
        raise HTTPException(status_code=400, detail="Project does not exist")

    # Optional: check for duplicate name within a project
    existing = (
        db.query(Asset)
        .filter(Asset.project_id == payload.project_id, Asset.name == payload.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Asset with this name already exists in this project",
        )

    asset = Asset(
        project_id=payload.project_id,
        name=payload.name,
        type=payload.type,
        # You *could* set project_name = project.name here if you keep the column
        project_name=project.name,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset