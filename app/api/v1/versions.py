from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Version, Asset
from app.schemas.version import VersionOut, VersionCreate

router = APIRouter(prefix="/versions", tags=["versions"])


@router.get("/", response_model=List[VersionOut])
def list_versions(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """List all versions for a specific asset."""
    versions = (
        db.query(Version)
        .filter(Version.asset_id == asset_id)
        .order_by(Version.version_number.desc())
        .all()
    )
    return versions


@router.post("/", response_model=VersionOut, status_code=201)
def create_version(payload: VersionCreate, db: Session = Depends(get_db)):
    """Create a new version for an asset (minimal publish record)."""

    # Ensure asset exists
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=400, detail="Asset does not exist")

    # Determine next version number for this asset
    latest = (
        db.query(Version)
        .filter(Version.asset_id == payload.asset_id)
        .order_by(Version.version_number.desc())
        .first()
    )
    next_version = (latest.version_number + 1) if latest else 1

    version = Version(
        asset_id=payload.asset_id,
        file_path=payload.file_path,
        comment=payload.comment,
        version_number=next_version,
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version