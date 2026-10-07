from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models import Version, Asset
from backend.app.schemas.version import VersionOut, VersionCreate

router = APIRouter(prefix="/versions", tags=["versions"])

@router.get("/", response_model=List[VersionOut])
def list_versions(
    asset_id: int,
    db: Session = Depends(get_db)):
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


    # Determine next version number for this version
    latest = (
        db.query(Version)
        .order_by(Version.version_number.desc())
        .first()
    )

    if not latest:
        latest = 1

    print("Troubleshooting:")
    print(f"Latest version found: {latest}")  # Add this to debug

    next_version = (latest.version_number + 1) if latest else 1

    version = Version(
        file_path=payload.file_path,
        comment=payload.comment,
        version_type=payload.version_type,
        department=payload.department,
        id=next_version,
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version