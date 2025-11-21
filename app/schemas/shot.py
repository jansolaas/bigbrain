from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShotBase(BaseModel):
    project_id: int
    sequence_id: int   # Required now
    name: str
    frame_start: Optional[int] = None
    frame_end: Optional[int] = None
    fps: Optional[float] = None


class ShotCreate(ShotBase):
    """Schema for creating a shot."""
    pass


class ShotOut(ShotBase):
    """Schema for reading a shot."""
    id: int

    model_config = ConfigDict(from_attributes=True)