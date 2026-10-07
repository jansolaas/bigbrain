from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.app.models.versions import VersionType

class VersionBase(BaseModel):
    asset_id: int
    file_path: str
    comment: Optional[str] = None
    version_type: VersionType  # or str, if more dynamic
    department: str
    task: str


class VersionCreate(VersionBase):
    """Schema for creating a version."""
    pass


class VersionOut(VersionBase):
    """Schema for reading a version."""
    id: int
    version_number: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)