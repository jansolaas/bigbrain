from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShotBase(BaseModel):
    project_id: int
    sequence_id: int   # Required now
    name: str
    frame_start: Optional[int] = None
    frame_end: Optional[int] = None
    fps: Optional[float] = None
    is_active: bool = True


class ShotCreate(ShotBase):
    """Schema for creating a shot."""
    pass

class ShotUpdate(BaseModel):
    """Schema for updating a shot (all fields optional)."""
    project_id: Optional[int] = None
    sequence_id: Optional[int] = None
    name: Optional[str] = None
    frame_start: Optional[int] = None
    frame_end: Optional[int] = None
    fps: Optional[float] = None
    is_active: Optional[bool] = None  # This allows toggling omitting

class ShotOut(ShotBase):
    """Schema for reading a shot."""
    id: int

    model_config = ConfigDict(from_attributes=True)